import boto3
from PIL import Image

def crop(image_path, coords, saved_location):
  """
  @param image_path: The path to the image to edit
  @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
  @param saved_location: Path to save the cropped image
  """
  image_obj = Image.open(image_path)
  cropped_image = image_obj.crop(coords)
  cropped_image.save(saved_location)
  cropped_image.show()

def uploadfile(sourcefile, bucket_name, folder):
  """
  @param sourcefile: Filename to be uploaded
  @param bucket_name: S3 bucket name
  @param folder: Path to upload the file
  """
  s3 = boto3.client('s3',)
  filename = sourcefile.split('\\')[1]
  transfer = S3Transfer(s3)
  data = open(sourcefile, 'rb')
  return transfer.upload_file(sourcefile , bucket_name, '{}/{}'.format(folder, filename))


def downloadfile(bucket_name, folder, filename):
  """
  @param bucket_name: S3 bucket name
  @param folder: Folder name
  @param filename: Filename
  """
  client = boto3.client('s3',)
  transfer = S3Transfer(client)
  # Download s3://bucket/key to /tmp/myfile
  transfer.download_file(bucket_name, filename, '/tmp/{}'.format(filename))


