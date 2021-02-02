import hashlib
import arcade



class TextureLoader():

    _textures = {}

    @staticmethod
    def get_texture(filepath, x, y, w, h, flip_h, flip_v, hit_box_algo, use_cache=True):
        # create hash from parameters
        hsh = hashlib.md5()
        hsh.update(f"{filepath}{x}{y}{w}{h}{flip_h}{flip_v}{hit_box_algo}".encode())
        id = hsh.hexdigest()
        # check if the texture is already present in the loader
        if use_cache and id in TextureLoader._textures:
            # Retrieve the cached texture
            tex = TextureLoader._textures[id]
        else:
            # Create genuine texture
            tex = arcade.load_texture(
                            filepath,
                            x, y, w, h,
                            flipped_horizontally=flip_h,
                            flipped_vertically=flip_v,
                            hit_box_algorithm=hit_box_algo)
            # Store texture only if requested
            if use_cache:
                TextureLoader._textures[id] = tex
        # Return either cached or newly created texture
        return tex


class AnimatedSprite(arcade.Sprite):

    """"
    New class for Sprite animation. (trial)
    """
    _current_animation_name: str

    # Private methods
    def _prepare_data_struct(self, frame_duration, back_and_forth, loop_counter, filter_color):
        return {
            "texture_list": [],
            "frame_duration": frame_duration,
            "back_and_forth": back_and_forth,
            "counter": loop_counter,
            "color": filter_color,
        }

    def _get_nb_frames(self,anim_name):
        """
        Private method to get the number of frames for the requested animation name
        :param str anim_name: name of the requested animation
        :return: tuple (int, int, int) number of textures, number of frames when back and forth is enabled, number of frames when counter is enabled (and back and forth)
        """
        nb_frames = 0
        nb_frames_baf = 0
        nb_frames_cnt = 0
        if anim_name in self._anims[self.state-1]:
            anim_dict = dict(self._anims[self.state-1][anim_name])
            nb_frames     = len(anim_dict["texture_list"])
            nb_frames_baf = nb_frames
            nb_frames_cnt = nb_frames
            if anim_dict["back_and_forth"]:
                nb_frames_baf += nb_frames - 2
            if anim_dict["counter"] > 0:
                nb_frames_cnt = nb_frames_baf*anim_dict["counter"]
        return (nb_frames, nb_frames_baf, nb_frames_cnt)

    def _get_frame_index(self, anim_name):
        """
        Private methods to get the current index to display and the percentage of progression in the requested animation
        :param anim_name: name of the requested animation
        :return: tuple(int, float) index of the frame to display, percentage progression
        """
        frame_idx  = 0
        frame_perc = 0
        if anim_name in self._anims[self.state-1]:
            anim_dict = self._anims[self.state-1][anim_name]
            # Get number of frames
            nb_frames, nb_frames_baf, nb_frames_cnt = self._get_nb_frames(anim_name)
            # compute absolute frame index according to time
            frame_idx = int(self._elapsed_duration / anim_dict["frame_duration"])
            # update frame index according to loop counter
            if anim_dict["counter"] <= 0:
                # use modulo for infinite loop
                frame_idx = frame_idx % nb_frames_baf
            else:
                # Saturate the final index frame (stay on the last frame)
                frame_perc = min(1.0, frame_idx / nb_frames_cnt)
                if frame_idx >= nb_frames_cnt:
                    frame_idx = nb_frames_cnt - 1
                frame_idx  = frame_idx % nb_frames_baf
            # In case of back And Forth
            if frame_idx >= nb_frames:
                frame_idx = nb_frames_baf - frame_idx
        return frame_idx, frame_perc



    # Constructor
    def __init__(self):
        #call to parent (Sprite)
        super().__init__()

        # parent fields
        self.state = arcade.FACE_RIGHT

        # animation data structure
        # First a list of dictionnaries, one entry for one state value
        # Each dictionary entry contains the following :
        # - KEY : name of the animation,
        # - VALUE = dict {
        #     + texture_list : []
        #     + frame_duration : float
        #     + back_and_forth : bool
        #     + counter : int
        #    }
        self._anims = [{},{},{},{}]

        # Current animation name
        self._current_animation_name = None
        # Current displayed texture
        self.cur_texture_index = 0
        # Set elapsed duration (used to know if we have to stop the animation)
        self._elapsed_duration = 0
        # Set play/pause flag
        self._playing = True
        # Percentage progression
        self._percent_progression = 0

    def add_animation(self,
                     animation_name: str,
                     filepath: str,
                     nb_frames_x: int,
                     nb_frames_y: int,
                     frame_width: int,
                     frame_height: int,
                     frame_start_index: int = 0,
                     frame_end_index: int = 0,
                     frame_duration: float = 1 / 24,
                     flipped_horizontally: bool = False,
                     flipped_vertically: bool = False,
                     loop_counter: int = 0,
                     back_and_forth: bool = False,
                     filter_color: tuple = (255, 255, 255, 255),
                     facing_direction: int = arcade.FACE_RIGHT,
                     hit_box_algo: str = 'None',
                     use_cache = True
                     ):
        """
        Adds a new animation in the Sprite object. It takes all images from a given SpriteSheet. \
        This Sprite is animated according to the elpased time and each frame has the same duration. \
        If this animation is the first to be added, select it right now.
        :param str filepath: path to the image file.
        :param int final_width: final width of the sprite (after input image has been resized).
        :param int final_height: final height of the sprite (after input image has been resized).
        :param bool use_max_ratio: flag to indicate if the resize operation will keep the whole sprite \
        in the final_width and final_height box (False), or if it will fill the complete box, \
        even if one of the dimensions will get out of the box. In both cases, the aspect ratio will be kept. \
        In all cases, the final_width and the final_height values may not been respected, depending on final \
        size ratio and input image ratio.
        :param int nb_frames_x: number of frames in the input image, along the x-axis
        :param int nb_frames_y: number of frames in the input image, along the y-axis
        :param int frame_start_index: index of the first frame of the current animation. Indexes start at 0. \
        Indexes are taken from left to right and from top to bottom. 0 means the top-left frame in the input image.
        :param int frame_end_index: index of the last frame for the current animation. this value cannot exceed (nb_frames_x*nb_frames_y)-1.
        :param float frame_duration: duration of each frame (in seconds).
        :param bool flipped_horizontally: flag to indicate the frames will be horizontally flipped for this animation.
        :param bool flipped_vertically: flag to indicate the frames will be vertically flipped for this animation.
        :param int loop_counter: integer value to tell how many animation loop must be performed before the animation is being stopped. \
        If the value is zero or less, that means the animation will loop forever. When an animation has finished, it remains on the last frame.
        :param bool back_and_forth: flag to indicate if the frames used in this animation (with indexes between frame_start_index and frame_end_index) \
        must be duplicated in the opposite order. It allows a sprite sheet with 5 frames, '1-2-3-4-5', to create an animation like, \
        either '1-2-3-4-5' (flag value = False) \
        or '1-2-3-4-5-4-3-2' (flag value to True).
        :param tuple filter_color: RGBA tuple to be used like a filter layer. All the frames used in this animation will be color-filtered.
        :param str animation_name: functional name of your animation. This string will be used to select the animation you want to display. \
        If you have several animations, one per facing direction, you can give the same name for all of these animations (e.g. 'walk'/'run'/'idle'). \
        This is the pair 'animation_name'+'facing_direction' that will be used to select the correct frame to display
        :param int facing_direction: current facing direction for your animated sprite. It will be used in addition with animation_name, \
        in order to select the correct frame to display. Warning : if one pair 'animation_name'+'facing_direction' is missing in the animation \
        data structure (e.g. you didn't add this animation), the previous selected animation will remain selected.
        :param bool flag used to avoid recreating existing textures, previously loaded.
        :return None
        """

        # Create data structure if not already existing
        if animation_name in self._anims[facing_direction-1]:
            raise RuntimeError(f"AnimatedSprite : {animation_name} is already added to the current object (state={facing_direction})")

        my_dict = self._prepare_data_struct(frame_duration,back_and_forth,loop_counter,filter_color)

        # Now create all textures and add them into the list
        direction = "forward"
        if frame_start_index > frame_end_index:
            direction = "backward"
        for y in range(nb_frames_y):
            for x in range(nb_frames_x):
                index = x + (y * nb_frames_x)
                # add index only if in range
                index_ok = False
                if direction =="forward" and index >= frame_start_index and index <= frame_end_index:
                        index_ok = True
                elif direction =="backward" and index >= frame_end_index and index <= frame_start_index:
                        index_ok = True
                if index_ok:
                    # create texture
                    tex = TextureLoader.get_texture(
                            filepath,
                            x*frame_width, y*frame_height,
                            frame_width, frame_height,
                            flipped_horizontally,
                            flipped_vertically,
                            hit_box_algo,
                            use_cache)
                    # Store texture in the texture list
                    if direction == "forward":
                        my_dict["texture_list"].append(tex)
                    else:
                        my_dict["texture_list"] = [tex,] + my_dict["texture_list"]

        # Store this animation
        self._anims[facing_direction-1][animation_name] = my_dict

        # If this animation is the first, select it, and select the first texture, and play
        if self._current_animation_name == None:
            self.select_animation(animation_name, True, True)
            self.update_animation(0)

    def select_animation(self, animation_name, rewind=False, running=True):
        """
        Select the current animation to display. \
        This method only checks if there is an animation with the given name in the data structure, \
        for the current facing direction. \
        If yes, this animation is selected, and the Sprite class textures field is updated. If not, this method does nothing.
        :param str animation_name: just the functional name of the animation to select.
        :param bool rewind: a flag to indicate if the new animation must be rewind or not. By default no rewind is done.
        :param bool runnning: a flag to indicate if the new animation must be played or stopped. By default the animation is played.
        :return: None
        """
        if animation_name in self._anims[self.state-1]:
            self._current_animation_name = animation_name
            data_struct = dict(self._anims[self.state-1][animation_name])
            self.textures = data_struct["texture_list"]
            self.color = data_struct["color"]
            if rewind:
                self.rewind_animation()
            if running:
                self.resume_animation()

    def select_frame(self, frame_index):
        """
        This method selects a specific frame in the stored textures.\
        When calling this method, it automatically pauses the animation.
        In other words, this method forces the current class behaviour.
        :param int frame_index: number of the requested frame.
        :return: None
        """
        self.pause_animation()
        self.cur_texture_index = frame_index
        self.set_texture(self.cur_texture_index)
        self._percent_progression = 0

    def removeAnimation(self, anim_name):
        # remove animations from the data structure
        for facing_direction in range(0,4):
            if anim_name in self._anims[facing_direction]:
                del self._anims[facing_direction][anim_name]
        # check if this animation was the current one selected
        # if yes just raise an error in order to notify the developper
        # to onlyremove unused animations
        if anim_name == self._current_animation_name:
            raise RuntimeError(f"[ERR] AnimatedSprite : remove animation only is not used {anim_name}")

    def update_animation(self, delta_time: float = 1/60):
        # Increase current elapsed time if playing
        if self._playing:
            self._elapsed_duration += delta_time

            # If the current animation name is not found in the state list, that means
            # the state has been changed after anim selection. So now we do not update anymore.
            # else, just process
            if self._current_animation_name in self._anims[self.state-1]:
                # Get current frame index
                frame_idx, frame_perc = self._get_frame_index(self._current_animation_name)
                # set current texture index and texture from the parent class
                data_struct = dict(self._anims[self.state - 1][self._current_animation_name])
                self.textures = data_struct["texture_list"]
                self.cur_texture_index = frame_idx
                self.set_texture(self.cur_texture_index)
                # Store current percentage
                self._percent_progression = frame_perc

    def pause_animation(self):
        """
        Pauses the current animation. It does not rewind it.
        :return: None
        """
        self._playing = False

    def resume_animation(self):
        """
        Resumes the current animation. It does not rewind it.
        :return: None
        """
        self._playing = True

    def rewind_animation(self):
        """
        Just rewinds the current animation to the first frame. It does not change the play/stop flag.
        :return: None
        """
        self._elapsed_duration = 0

    def play_animation(self):
        """
        Rewinds and Plays the current animation.
        :return: None
        """
        self.rewind_animation()
        self.resume_animation()

    def stop_animation(self):
        """
        Stops the current animation and rewinds it.
        :return: None
        """
        self.pause_animation()
        self.rewind_animation()

    def get_current_animation(self):
        return self._current_animation_name

    def is_finished(self):
        return self._percent_progression >= 1.0

    def get_percent(self):
        return self._percent_progression
        pass
