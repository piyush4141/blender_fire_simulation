import random
class cfg:
    def __init__(self):
        # background image folder path
        self.folder_path =  "/content/drive/MyDrive/blender_fire/background_Images"

        # light
        self.min_light = 1
        self.max_light = 3
        self.energy = 2.19326

        # smoke object

        self.smoke_obj = {
            'flow_settings': {
                'fuel_amount': ((1,10),"float"),
                'flow_type': 'FIRE',

            }
        }

        # smoke domain
        self.smoke_dom = {
            'settings': {
                'domain_type': 'GAS',
                'resolution_max': ((3,64),'int'),
                'time_scale': ((1,10),"float")
            }, 'Gas': {'dissolve_speed': ((1,1000),'int'),
                       'noise_pos_scale': ((1,10),"float")
                       }

        }
        self.fuel_amount = 5  # (rangen 1,10)

        self.fire_resolution = 64  # for loop on  resolution range (6,6+2,128)
        # Time Scale controls the speed of the simulation.
        # Low values result in a “slow motion” simulation, while higher values result in a “faster motion”.

        ## for loop on  time scale range (0,0.10,10)
        self.time_scale = 1.1

        self.use_dissolve_smoke = True
        ## for loop on disslove(1,10000)
        self.dissolve_speed = 16

        '''smoke density loop'''
        self.smoke_density = 200
        self.black_body_intensity = 10
        # noise
        self.use_noise = True

        ## for loop on noise sacle(0,10)
        self.noise_pos_scale = 4.10


        '''colour setting'''
        # smoke_obj.modifiers["Fluid"].domain_settings.flame_smoke_color = (226, 88, 34)

        #  RENDERING CONFIG\
        self.render_engine = 'CYCLES'
        self.cycles_device = 'GPU'
        self.output_format = 'PNG'
        self.color_mode = 'RGBA'
        self.compression = 90
        self.resolution_x = 640  # pixel resolution
        self.resolution_y = 360
        # self.samples = 512  # render engine samples
        self.start_frame = 1
        self.end_frame = 130
        #  OUTPUT FOLDER
        self.output_dir =  "/content/drive/MyDrive/blender_fire/synthetic_fire_data"