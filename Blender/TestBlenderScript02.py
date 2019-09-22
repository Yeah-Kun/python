import bpy
import numpy as np
from PIL import Image


class CarModelViewToImage():
    # def __init__:
    #     self.camera_ = None
    #     self.image_folder_ = None
    #     self.car_width_ = 0
    #     self.car_length_ = 0
    #     self.viewport_width_ = 0
    #     self.viewport_height_ = 0
    #     self.stride_ = 0
    #     self.stride_radians_ = 0
    #     self.car_ = None
    #     self.scene_length_ = 0
    #     self.scene_height_ = 0
    #     self.light_ctr_ = None

    def init(self, info):
        """
            info: { 
                "car_width" : float,
                "car_length": float,
                "viewport_width"  : float,
                "viewport_height" : float,
                "image_folder" : string
                }
        """
        # get base information
        self.car_width_ = info["car_width"]
        self.car_length_ = info["car_length"]
        self.viewport_width_ = info["viewport_width"]
        self.viewport_height_ = info["viewport_height"]
        self.image_folder_ = info["image_folder"]
        self.scene_length_ = self.car_length_ * 2
        self.scene_height_ = self.car_length_
        
        bpy.context.scene.render.resolution_x = self.viewport_width_
        bpy.context.scene.render.resolution_y = self.viewport_height_
        bpy.context.scene.render.filepath = self.image_folder_

        # resize model and light
        # save model dimensions and location
        self.car_ = bpy.data.objects["car"]

        # save light location
        self.light_ctr_ = [bpy.data.objects["left_light"],
                           bpy.data.objects["right_light"], bpy.data.objects["top_light"]]

        # move model and light
        offset = self.car_.location.copy()
        self.car_.location -= offset

        for l in self.light_ctr_:
            l.location -= offset

        # calculate prop from length and resize
        car_length_now = max(self.car_.dimensions)
        scale_size = self.car_length_ / car_length_now

        self.car_.scale *= scale_size
        for l in self.light_ctr_:
            l.location *= scale_size
            l.scale *= scale_size

        # set camera
        bpy.ops.object.camera_add()
        self.camera_ = bpy.data.objects["Camera"]
        # set camera base info
        self.camera_.data.lens_unit = "FOV"
        self.camera_.data.angle = np.radians(90)
        self.camera_.data.clip_start = 0.1
        self.camera_.data.clip_end = self.scene_length_ * 2

        # set camera constraint
        bpy.ops.object.constraint_add(type="TRACK_TO")
        bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'
        bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        bpy.context.object.constraints["Track To"].target = self.car_
        bpy.context.object.constraints["Track To"].use_target_z = True


        # set render Node
        self.scene_ = bpy.context.scene
        self.scene_.use_nodes = True
        self.tree_ = self.scene_.node_tree
        self.links_ = self.tree_.links

        # clear default nodes
        for n in self.tree_.nodes:
            self.tree_.nodes.remove(n)

        self.render_layer_ = self.tree_.nodes.new('CompositorNodeRLayers')
        self.viewer_image_ = self.tree_.nodes.new('CompositorNodeViewer')
        self.viewer_image_.use_alpha = False


    def set_camera_pos(self, x, y, z=None):
        # 计算真实坐标
        real_x = np.clip(x, -1, 1) * self.scene_length_
        real_y = np.clip(y, -1, 1) * self.scene_length_
        self.camera_.location[0] = real_x
        self.camera_.location[1] = real_y

        if(z != None):
            real_z = np.clip(z, 0, 1) * self.scene_height_
            self.camera_.location[2] = real_z


    def render_image(self, img_name, folder_path):
        """
            渲染图像
        """
        filepath = folder_path + img_name
        filepath_depth = folder_path + "z" + img_name

        # color
        self.links_.clear()
        self.links_.new(self.render_layer_.outputs[0], self.viewer_image_.inputs[0])
        bpy.ops.render.render()
        bpy.data.images[0].save_render(filepath)


        # depth
        self.links_.clear()
        # self.links_.new(self.render_layer_.outputs["Depth"], self.viewer_depth_.inputs[0])
        self.links_.new(self.render_layer_.outputs["Depth"], self.viewer_image_.inputs[0])
        bpy.ops.render.render()
        
        pixels = bpy.data.images['Viewer Node'].pixels
        pixels = np.array(pixels)[::4][::-1] # get the pixels
        pixels[pixels < 10000000000.0] = 255
        pixels[pixels >= 10000000000.0] = 0

        pix = pixels.astype(dtype=np.uint8).reshape((self.viewport_height_, self.viewport_width_))
        img = Image.fromarray(pix)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        img.save(filepath_depth)


    def get_single_image(self, x, y, z, img_name, folder_path=""):
        """
            x,y,z:摄像头位置在场景的比例，其中x、y为-1~1，z为0~1 
            img_name : 文件名
            folder_path : 文件夹路径
        """
        # 设置摄像机
        self.set_camera_pos(x,y,z)

        # 渲染并保存图像
        bpy.context.scene.camera = self.camera_
        bpy.ops.render.render()

        self.render_image(img_name, folder_path)
        if(folder_path != ""):
            self.render_image(img_name, folder_path)
        else:
            self.render_image(img_name, self.image_folder_)


    def get_surround_image(self, xy, z, rotate_stride, folder_path = ""):
        """
            x,y,z:摄像头位置在场景的比例，其中x、y为-1~1，z为0~1 
            rotate_stride : 旋转的角度
            folder_path : 文件夹路径
        """
        def set_camera_pos(angle, camera_to_origin_length):
            self.camera_.location[0] = camera_to_origin_length * np.cos(np.radians(angle))
            self.camera_.location[1] = camera_to_origin_length * np.sin(np.radians(angle))


        # 计算旋转角度相关信息
        bpy.context.scene.camera = self.camera_
        self.stride_ = rotate_stride
        self.stride_radians_ = np.radians(rotate_stride)
        
        # set camera parameters
        self.set_camera_pos(xy, 0, z)
        real_xy = self.scene_length_ * np.clip(xy, -1, 1)
        real_z = self.scene_height_ * np.clip(z, 0, 1)
        camera_length = np.sqrt(real_xy**2 + real_z**2)

        
        for i in range(0, 360, rotate_stride):
            img_name = str(i) + ".jpg"
            set_camera_pos(i, camera_length)

            bpy.context.scene.camera = self.camera_
            bpy.ops.render.render()
            if(folder_path != ""):
                self.render_image(img_name, folder_path)
            else:
                self.render_image(img_name, self.image_folder_)



if __name__ == '__main__':
    info = {
        "car_width" : 30,
        "car_length": 50,
        "viewport_width"  : 1280,
        "viewport_height" : 720,
        "image_folder" : "E:/company/MyWork/Workspace/CPU_3D/resources/Huake8296/car_image/single/"
    }

    car_view = CarModelViewToImage()
    car_view.init(info)
    #car_view.get_single_image(0, 0, 1, "top_view.jpg")# have a bug
    #car_view.get_surround_image(-0.6, 0.4, 90)
    car_view.get_single_image(0, -0.6, 0.6, "view_front.jpg")
    car_view.get_single_image(0,  0.6, 0.6, "view_back.jpg")
    car_view.get_single_image(0.6, 0, 0.6, "view_left.jpg")
    car_view.get_single_image(-0.6, 0, 0.6, "view_right.jpg")
    
    car_view.get_single_image(0.6, -0.6, 0.6, "view_left_front.jpg")
    car_view.get_single_image(0.6, 0.6, 0.6, "view_left_back.jpg")
    car_view.get_single_image(-0.6, -0.6, 0.6, "view_right_front.jpg")
    car_view.get_single_image(0.6, -0.6, 0.6, "view_right_back.jpg")
    
    
    
    