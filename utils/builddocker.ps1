# Usage: ./builddocker.ps1 [-file name_of_your_docker_file | -project name_of_docker_image_to_build]
# Parameters are optional, if not provided default values will be used
# You can replace default values with your file and project names
param ($file = 'minimal.Dockerfile', $project = 'youtubetrends')
write-host "Please wait. Building docker image using: $file"
docker build -t $project install/ -f install/$file
write-host "Done. Docker image $project created"