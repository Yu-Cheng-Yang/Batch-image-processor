from datetime import datetime
import os

from PIL import Image
import piexif

class ExifDisplayInformation():
    def __init__(self, file = None, image = None, exif_dict = None):
        self.exif_dict = None

        if file and isinstance(file, str):
            _, self.exif_dict = self._load_image(file) 
        elif image and isinstance(file, Image):
            image_exif_info = image.info['exif'] if 'exif' in image.info else None
            self.exif_dict = piexif.load(image_exif_info) if image_exif_info else None
        else:
            self.exif_dict = exif_dict
        
        self.init_maps()

    def init_maps(self):
        self.display_map = {
            piexif.ImageIFD.Orientation : { 1 : "Horizontal (normal)",
                                            2 : "Mirror horizontal",
                                            3 : "Rotate 180",
                                            4 : "Mirror vertical",
                                            5 : "Mirror horizontal and rotate 270 CW",
                                            6 : "Rotate 90 CW",
                                            7 : "Mirror horizontal and rotate 90 CW",
                                            8 : "Rotate 270 CW"
                                          },
            piexif.ImageIFD.ResolutionUnit : { 2 : 'Inches', 3: 'Centimeters'},
            piexif.ImageIFD.YCbCrPositioning : { 1 : 'Centered', 2 : 'Co-sited'},
            piexif.ExifIFD.ExposureProgram : { 0 : "Not Defined",
                                               1 : "Manual",
                                               2 : "Normal Program",
                                               3 : "Aperture Priority",
                                               4 : "Shutter Priority",
                                               5 : "Creative Program(Slow speed)",
                                               6 : "Action Program(High speed)",
                                               7 : "Portrait Mode",
                                               8 : "Landscape Mode",
                                               9 : "Bulb",
                                            },
            piexif.ExifIFD.MeteringMode : { 0 : "Unknown",
                                            1 : "Average",
                                            2 : "Center Weighted Average",
                                            3 : "Spot",
                                            4 : "MultiSpot",
                                            5 : "Pattern",
                                            6 : "Partial",
                                            255 : "Other"
                                          },
            piexif.ExifIFD.ComponentsConfiguration : {0: '-',
                                                      1 : 'Y',
                                                      2 : 'Cb',
                                                      3 : 'Cr',
                                                      4 : 'R',
                                                      5 : 'G',
                                                      6 : 'B'},
            piexif.ExifIFD.SceneCaptureType : {0 : 'Standard',
                                               1 : 'Landscape',
                                               2 : 'Portrait',
                                               3 : 'Night scene'},
            piexif.GPSIFD.GPSAltitudeRef : {0 : "Above sea level",
                                            1 : 'Below sea level'},
            piexif.GPSIFD.GPSDestBearingRef : {'T' : 'True direction',
                                               'M' : 'Magnetic direction'},
            piexif.GPSIFD.GPSSpeedRef : {'K' : 'Kilometers per hour',
                                         'M' :'Miles per hour',
                                         'N' :'Knots'},
            piexif.GPSIFD.GPSImgDirectionRef : {'T' : 'True direction', 'M' : 'Magnetic direction'},
            piexif.GPSIFD.GPSLatitudeRef : {'N' : 'North', 'S' : 'South'},
            piexif.GPSIFD.GPSLongitudeRef : {'E' : 'East', 'W' : 'West'},
            piexif.ExifIFD.WhiteBalance: {0 : 'Auto White Balance',
                                          1 : 'Manual White Balance'},
            piexif.ImageIFD.SampleFormat: { 1 : 'Unsigned',
                                            2 : 'Signed',
                                            3 : 'Float',
                                            4 : 'Undefined ',
                                            5 : 'Complex int ',
                                            6 : 'Complex float'
                                           } ,
            piexif.ExifIFD.Flash : { 0 : 'Flash did not fire',
                                     1 : 'Flash fired',
                                     5 : 'Strobe return light not detected',
                                     7 : 'Strobe return light detected',
                                     9 : 'Flash fired, compulsory flash mode',
                                    13 : 'Flash fired, compulsory flash mode, return light not detected',
                                    15 : 'Flash fired, compulsory flash mode, return light detected',
                                    16 : 'Flash did not fire, compulsory flash mode',
                                    24 : 'Flash did not fire, auto mode',
                                    25 : 'Flash fired, auto mode',
                                    29 : 'Flash fired, auto mode, return light not detected',
                                    31 : 'Flash fired, auto mode, return light detected',
                                    32 : 'No flash function',
                                    65 : 'Flash fired, red-eye reduction mode',
                                    69 : 'Flash fired, red-eye reduction mode, return light not detected',
                                    71 : 'Flash fired, red-eye reduction mode, return light detected',
                                    73 : 'Flash fired, compulsory flash mode, red-eye reduction mode',
                                    77 : 'Flash fired, compulsory flash mode, red-eye reduction mode, return light not detected',
                                    79 : 'Flash fired, compulsory flash mode, red-eye reduction mode, return light detected',
                                    89 : 'Flash fired, auto mode, red-eye reduction mode',
                                    93 : 'Flash fired, auto mode, return light not detected, red-eye reduction mode',
                                    95 : 'Flash fired, auto mode, return light detected, red-eye reduction mode'
                                   }
        }

        self.skip_tag_set = {
            piexif.ExifIFD.MakerNote,
            piexif.ImageIFD.InterColorProfile
        }
        
         # exif section to piexif section map
        self.section_map = {
            '0th'  : 'Image',
            '1st'  : 'Image',
            'Exif' : 'Exif',
            'GPS'  : 'GPS',
            'InterOp' : 'InterOp'
        }
        
        self.camera_set = {
            piexif.ImageIFD.Make,
            piexif.ImageIFD.Model,
            piexif.ExifIFD.FNumber,
            piexif.ExifIFD.ExposureTime,
            piexif.ExifIFD.ExposureProgram,
            piexif.ExifIFD.ISOSpeedRatings,
            piexif.ExifIFD.ExposureBiasValue,
            piexif.ExifIFD.MaxApertureValue,
            piexif.ExifIFD.ApertureValue,
            piexif.ExifIFD.FocalLength,
            piexif.ExifIFD.MeteringMode,
            piexif.ExifIFD.MeteringMode,
            piexif.ExifIFD.SubjectDistance,
            piexif.ExifIFD.Flash,
            piexif.ExifIFD.FlashpixVersion,
            piexif.ExifIFD.FocalLengthIn35mmFilm,
            piexif.ExifIFD.LensMake,
            piexif.ExifIFD.LensModel,
            piexif.ExifIFD.LensSpecification,
            piexif.ExifIFD.LensSerialNumber,
            piexif.ExifIFD.SceneCaptureType,
            piexif.ExifIFD.SceneType,
            piexif.ExifIFD.WhiteBalance,
            piexif.ExifIFD.ExposureMode,
            piexif.ExifIFD.SensingMethod
        }

        self.image_set = {
            piexif.ExifIFD.PixelXDimension,
            piexif.ExifIFD.PixelYDimension,
            piexif.ImageIFD.ImageLength,
            piexif.ImageIFD.ImageWidth,
            piexif.ImageIFD.ImageLength,
            piexif.ExifIFD.ColorSpace,
            piexif.ImageIFD.Compression,
            piexif.ImageIFD.XResolution,
            piexif.ImageIFD.YResolution,
            piexif.ImageIFD.ResolutionUnit,
            piexif.ImageIFD.YCbCrPositioning,
            piexif.ImageIFD.JPEGInterchangeFormat,
            piexif.ImageIFD.JPEGInterchangeFormatLength,
            piexif.ExifIFD.ComponentsConfiguration,
            piexif.ImageIFD.Software,
            piexif.ImageIFD.Orientation
        }

        self.gps_set = {
            piexif.GPSIFD.GPSVersionID,
            piexif.GPSIFD.GPSLatitudeRef,
            piexif.GPSIFD.GPSLatitude,
            piexif.GPSIFD.GPSLongitudeRef,
            piexif.GPSIFD.GPSLongitude,
            piexif.GPSIFD.GPSAltitude,
            piexif.GPSIFD.GPSAltitudeRef,
            piexif.GPSIFD.GPSSpeed,
            piexif.GPSIFD.GPSSpeedRef,
            piexif.GPSIFD.GPSTrackRef,
            piexif.GPSIFD.GPSTrack,
            piexif.GPSIFD.GPSImgDirectionRef,
            piexif.GPSIFD.GPSImgDirection,
            piexif.GPSIFD.GPSMapDatum,
            piexif.GPSIFD.GPSDestLatitudeRef,
            piexif.GPSIFD.GPSDestLatitude,
            piexif.GPSIFD.GPSDestLongitudeRef,
            piexif.GPSIFD.GPSDestLongitude,
            piexif.GPSIFD.GPSDestBearingRef,
            piexif.GPSIFD.GPSDestBearing,
            piexif.GPSIFD.GPSDestDistanceRef,
            piexif.GPSIFD.GPSDestDistance,
            piexif.GPSIFD.GPSProcessingMethod,
            piexif.GPSIFD.GPSAreaInformation,
            piexif.GPSIFD.GPSDifferential,
            piexif.GPSIFD.GPSHPositioningError,
            piexif.ImageIFD.GPSTag
        }

        self.date_time_set = {
            piexif.ImageIFD.DateTime,
            piexif.ExifIFD.DateTimeOriginal,
            piexif.ExifIFD.DateTimeDigitized,
            piexif.ExifIFD.OffsetTime,
            piexif.ExifIFD.OffsetTimeOriginal,
            piexif.ExifIFD.OffsetTimeDigitized,
            piexif.GPSIFD.GPSDateStamp,
            piexif.GPSIFD.GPSTimeStamp,
            piexif.ExifIFD.SubSecTime,
            piexif.ExifIFD.SubSecTimeDigitized,
            piexif.ExifIFD.SubSecTimeOriginal
        }

        self.special_name_map = {
            'YCbCrPositioning':'YCbCr Positioning',
            'PixelXDimension' : 'Pixel X Dimension',
            'PixelYDimension' : 'Pixel Y Dimension',
            'GPSHPositioningError': 'GPS H Positioning Error'
        }
        
        self.tuple_format_map = {
            piexif.GPSIFD.GPSAltitude : '%06f m',
            piexif.ExifIFD.FocalLength:'%.02f mm',
            piexif.ExifIFD.ApertureValue:'%.02f',
            piexif.ExifIFD.FNumber:'f/%.02f',
            piexif.ExifIFD.BrightnessValue:'%.06f',
            piexif.ExifIFD.ExposureBiasValue:'%.02f'
        }
        
    def get_original_dict(self):
        return self.exif_dict
    
    def get_display_dict(self):
        display_dict = {'Image':{}, 'Date and Time' : {}, 'Camera':{}, 'GPS':{}, 'Others': {}}
        self._get_section_display_dict('0th', display_dict)
        #display_dict['Image'] = dict_0th
        
        self._get_section_display_dict('1st', display_dict)
        #display_dict['Image'].update(dict_1st)

        self._get_section_display_dict('Exif', display_dict)
        #display_dict['Exif'] = dict_exif

        self._get_section_display_dict('GPS', display_dict)
        #display_dict['GPS'] = dict_gps
        
        # Post process
        # Aperture Value is dependent on F Number
        camera_section = display_dict['Camera']
        if 'F Number' in camera_section:
            value = camera_section['F Number']
            camera_section['Aperture Value'] = value[2:]
        return display_dict

    def _load_image(self, filename):
        image = None
        exif_dict = None
        if os.path.isfile(filename):
            try:
                image = Image.open(filename)
            except:
                image = None
            if image:
                image_exif_info = image.info['exif'] if 'exif' in image.info else None
                exif_dict = piexif.load(image_exif_info) if image_exif_info else None
        return image, exif_dict

    def _get_special_tag_display_str(self, tag, value):
        disp_str = ''
        if tag == piexif.ExifIFD.ComponentsConfiguration:
            tag_value_map = self.display_map[piexif.ExifIFD.ComponentsConfiguration]
            for byte in value:
                if byte in tag_value_map:
                    disp_str = disp_str + tag_value_map[byte]
        if tag == piexif.ExifIFD.ShutterSpeedValue:
            if len(value) >= 2 and value[1] != 0:
                disp_str = '1/%d' % (int(2**(value[0] / value[1])))
        elif tag == piexif.ExifIFD.ExposureTime:
            if len(value) >= 2:
                disp_str = '%d/%d' %(value[0], value[1])
        elif tag == piexif.ExifIFD.SceneType:
            if value == b'\x01':
                disp_str = 'A directly photographed image' 
        elif tag == piexif.GPSIFD.GPSLatitude or tag == piexif.GPSIFD.GPSLongitude:
            length = len(value)
            degree = 0
            if length >= 1:
                degree += value[0][0] / value[0][1]
                if length >= 2:
                    degree += value[1][0] / (value[1][1] * 60)
                if length >= 3:
                    degree += value[2][0] / (value[2][1] * 3600)
                disp_str = '{:.6f}'.format(degree)
        elif tag == piexif.GPSIFD.GPSTimeStamp:
            t = [0, 0, 0]
            for index, v in enumerate(value):
                if len(v) >= 2 and v[1] != 0:
                    t[index] = int(v[0] / v[1])
            disp_str = '%02d:%02d:%02d' %(t[0], t[1], t[2])
        elif tag == piexif.ExifIFD.LensSpecification:
            result = [0, 0, 0, 0]
            for index, v in enumerate(value):
                if len(v) >= 2 and v[1] != 0:
                    result[index] = v[0] / v[1]
            disp_str = '%.02f-%.02f mm f/%.02f-%.02f' %(result[0], result[1], result[2], result[3])
        elif tag == piexif.GPSIFD.GPSVersionID:
            for index, v in enumerate(value):
                disp_str += '.%d' % v if index != 0 else '%d' % v 
        elif tag == piexif.ImageIFD.SampleFormat:
            map1 = self.display_map[tag]
            for index, v in enumerate(value):
                disp_str += ',%s' % map1[v] if index != 0 else '%s' % map1[v]
        elif tag == piexif.ImageIFD.StripOffsets:
            disp_str += str(value)
        elif tag == piexif.ExifIFD.SubjectArea:
            if len(value) == 2:
                disp_str = 'Coordinate: (%d, %d)' % (value[0], value[1])
            elif len(value) == 3:
                disp_str = 'Circle: Center: (%d, %d), Diameter: %d' % (value[0], value[1], value[2])
            elif len(value) == 4:
                disp_str = 'Rectangle: Center: (%d, %d), Width: %d, Height: %d' % (value[0], value[1], value[2], value[3])
        elif isinstance(value, tuple) and len(value) == 2 and value[1] != 0:
                value1 = value[0] / value[1]
                format = self.tuple_format_map[tag] if tag in self.tuple_format_map else '%06f' 
                disp_str = '0' if value1 == 0 else (format % value1)
        return disp_str

    def _get_section_display_dict(self, section_name, display_dict):
        if not self.exif_dict:
            return display_dict
        
        if section_name not in self.exif_dict:
            return display_dict
        
        piexif_tag_dict = piexif.TAGS[self.section_map[section_name]]
        exif_dict = self.exif_dict[section_name]
        
        for tag, value in exif_dict.items():
            if tag in self.skip_tag_set:
                continue
            try:
                dict = display_dict[self.get_tag_category(tag)]
                disp_str = self._get_special_tag_display_str(tag, value)
                if not disp_str:
                    if tag in self.display_map:
                        if isinstance(value, bytes):
                            value = value.decode()
                        disp_str = self.display_map[tag][value]
                    else:
                        if isinstance(value, bytes):
                            disp_str = value.decode()
                        else:
                            disp_str = str(value)
            except:
                print('tag %d with value %s' % (tag, str(value)))
            key = piexif_tag_dict[tag]['name']
            key = self.split_camel_case_proper(key)
            dict[key] = disp_str
            
        return display_dict

    def split_camel_case_proper(self, s):
        if s in self.special_name_map:
            return self.special_name_map[s]
        
        words = []
        start_index = 0
        for i in range(1, len(s)):
            if s[i].isupper() and (i + 1 == len(s) or s[i + 1].islower()):
                words.append(s[start_index:i])
                start_index = i
        words.append(s[start_index:])
        return ' '.join(words)

    def get_tag_category(self, tag):
        if tag in self.camera_set:
            return 'Camera'
        elif tag in self.image_set:
            return 'Image'
        elif tag in self.gps_set:
            return 'GPS'
        elif tag in self.date_time_set:
            return 'Date and Time'

        return 'Others'
