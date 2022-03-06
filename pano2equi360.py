import moderngl
import numpy as np
import math
import sys
from PIL import Image


start_image = Image.open(sys.argv[1])
start_width, start_height = start_image.size;

# Assuming radius in 1 unit
# width is equivlaent to 2*PI unit, so height of image is *height * 2 * PI) / width
# 

cylinder_height = (start_height * 2.0 * math.pi) / start_width;

ctx = moderngl.create_standalone_context()

input_texture = ctx.texture(start_image.size, 3, start_image.tobytes())
sampler = ctx.sampler(texture=input_texture) 

prog = ctx.program(
    vertex_shader='''
        #version 330

        in vec2 in_vert;
        in vec2 in_uv;
         
        out vec2 f_uv; 

        void main() {
            
            f_uv = in_uv; 
            gl_Position = vec4(in_vert , 0.0, 1.0);


        }
    ''',
    fragment_shader='''
        #version 330
        #define PI 3.1415926538

        uniform sampler2D Texture;
        uniform float cylinder_height;

        in vec2 f_uv;
 
        out vec4 f_color;

        void main() {

        // u should remain the same
        // convert v to polar angle, position on cylinder should be tan(angle) * cylinder height in units   

        vec2 final_uv = vec2(f_uv.x, f_uv.y); 
    
        // convert to angle after first recentering uv so 0,0 is in the middle
        final_uv.y -= 0.5f ; 
        final_uv.y *= PI ; 

        // tan(phi) = O/A , A is radius, assuming unit radius so O = tan(phi), O = height of cylinder from centre in units.
        final_uv.y = tan(final_uv.y);
        // convert that height back to uv cordinate on pano image.
        final_uv.y  /= cylinder_height; 
        final_uv.y  += 0.5f; 

        f_color = texture(Texture, final_uv);

       }
    ''',
)

in_corrections = prog['cylinder_height'];
in_corrections.value = cylinder_height;

vertices = np.array([
                1.0, 1.0,             1.0, 0.0, 
                -1.0, 1.0,            0.0, 0.0, 
                1.0, -1.0,            1.0, 1.0, 
                -1.0, -1.0,           0.0, 1.0, 
                -1.0, 1.0,            0.0, 0.0, 
                1.0, -1.0,            1.0, 1.0, 
])

vbo = ctx.buffer(vertices.astype('f4').tobytes())
vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_uv')

fbo = ctx.simple_framebuffer((4096,2048))
fbo.use()
fbo.clear(0.0, 1.0, 0.0, 1.0)

vao.scope = ctx.scope(framebuffer=fbo, samplers=[
            sampler.assign(0),
])



vao.render(moderngl.TRIANGLES)

fixed_image = Image.frombytes('RGB', fbo.size, fbo.read(), 'raw', 'RGB', 0, -1)
fixed_image.save(sys.argv[2])

