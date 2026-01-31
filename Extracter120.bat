set name=%1
mkdir .\camera_front
mkdir .\camera_left
mkdir .\camera_right
ffmpeg -y -i %name% ^
-vf "v360=input=e:output=e:h_fov=120:v_fov=120:yaw=0:pitch=0"   -s 2560x2560 -r 1 .\camera_right\%%06d.jpg ^
-vf "v360=input=e:output=e:h_fov=120:v_fov=120:yaw=-90:pitch=0" -s 2560x2560 -r 1 .\camera_front\%%06d.jpg ^
-vf "v360=input=e:output=e:h_fov=120:v_fov=120:yaw=-180:pitch=0" -s 2560x2560 -r 1 .\camera_left\%%06d.jpg
