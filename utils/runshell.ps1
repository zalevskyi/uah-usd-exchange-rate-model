# Usage: ./runshell.ps1 [-project name_of_docker_image_to_run]
# Parameter is optional, if not provided default value will be used
# You can replace default value with your project name
param ($project = 'youtubetrends')
write-host "Running with CPU only"
docker run -v ${PWD}:/tf -it --rm -p 8888:8888 $project bash