#
#         PySceneDetect: Python-Based Video Scene Detector
#   ---------------------------------------------------------------
#     [  Site: http://www.bcastell.com/projects/pyscenedetect/   ]
#     [  Github: https://github.com/Breakthrough/PySceneDetect/  ]
#     [  Documentation: http://pyscenedetect.readthedocs.org/    ]
#
# This file contains the SceneManager class, which provides a
# consistent interface to the application state, including the current
# scene list, user-defined options, and any shared objects.
#
# Copyright (C) 2012-2017 Brandon Castellano <http://www.bcastell.com>.
#
# PySceneDetect is licensed under the BSD 2-Clause License; see the
# included LICENSE file or visit one of the following pages for details:
#  - http://www.bcastell.com/projects/pyscenedetect/
#  - https://github.com/Breakthrough/PySceneDetect/
#
# This software uses Numpy and OpenCV; see the LICENSE-NUMPY and
# LICENSE-OPENCV files or visit one of above URLs for details.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#

# Standard Library Imports
from __future__ import print_function
import csv

import scenedetect.detectors


class SceneManager(object):

    # pylint: disable = too-few-public-methods, too-many-instance-attributes
    #
    # todo: this needs to take some high-level classes (to be defined) instead
    #       of just the CLI arguments.  then move the current __init__ method below
    #       to the cli.py file as a function to generate the appropriate classes
    #       to invoke the new constructor.
    

    #
    # The argument `scene_detectors` can be replaced with a reference directly
    # to the scenedetect.detectors (or perhaps make it just a default argument).
    #
    # Need to modify this to allow passing multiple detection methods as a list,
    # as opposed to just choosing a single one (based on the passed argument)
    # from the scene_detectors argument.  This will be unsupported at first,
    # but allowing a list of detectors to be passed instead of a single one
    # does make sense (and may work fine with properly designed detection
    # algorithm/method classes).
    #
    #def __init__(self, args, scene_detectors):
    def __init__(self, scene_detectors = None, args = None, detector = None,
                 stats_writer = None, downscale_factor = 1, frame_skip = 0,
                 save_images = False, start_time = None, end_time =  None,
                 duration = None, quiet_mode = False, perf_update_rate = -1):

        self.scene_list = list()
        self.args = args
        self.detector = detector
        self.cap = None
        self.perf_update_rate = perf_update_rate

        self.stats_writer = stats_writer
        self.downscale_factor = downscale_factor
        self.frame_skip = frame_skip
        self.save_images = save_images
        self.timecode_list = [start_time, end_time, duration]
        self.quiet_mode = False

        if self.args is not None:
            self._parse_args()

        self.detector_list = [ self.detector ]


    def _parse_args(self):
        
        args = self.args

        # Load SceneDetector with proper arguments based on passed detector (-d) if not specified.
        self.detector = None
        self.detection_method = args.detection_method.lower()
        scene_detectors = scenedetect.detectors.get_available()
        if not args.threshold:
            args.threshold = 30.0 if self.detection_method == 'content' else 12
        if (self.detection_method == 'content'):
            self.detector = scene_detectors['content'](args.threshold, args.min_scene_len)
        elif (self.detection_method == 'threshold'):
            self.detector = scene_detectors['threshold'](
                args.threshold, args.min_percent/100.0, args.min_scene_len,
                block_size = args.block_size, fade_bias = args.fade_bias/100.0)

        self.downscale_factor = args.downscale_factor
        if self.downscale_factor < 2:
            self.downscale_factor = 0

        self.frame_skip = args.frame_skip
        if self.frame_skip <= 0:
            self.frame_skip = 0

        self.save_images = args.save_images
        self.save_image_prefix = ''

        self.timecode_list = [args.start_time, args.end_time, args.duration]
        #self.start_frame = args.start_time
        #self.end_frame = args.end_time
        #self.duration_frames = args.duration

        self.quiet_mode = args.quiet_mode

        self.perf_update_rate = args.perf_update_rate

        if args.stats_file:
            self.stats_writer = csv.writer(args.stats_file)


    def clear(self):
        pass


    def detect_scenes(self, input_video = None):
        # need to move from __init__.py to this class.
        # if input_video is not specified, assume it was
        # set by the parse_cli_args method, and if not,
        # then throw an error.  (property is self.input_video)

        #
        # subsequent calls to this function should simply append the results to the existing
        # detected scene list, respecting the start/stop/seek times mentioned. it would be a
        # good idea to keep track of the number of frames processed (or current location timecode)
        # for subsequent calls to this function to keep track of the current "location" in a
        # stack of appended video files.
        #
        pass

