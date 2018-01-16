import os
import boto3
from PIL import Image
from boto3.s3.transfer import S3Transfer

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
  filename = sourcefile.split('/')[-1]
  transfer = S3Transfer(s3)
  data = open(sourcefile, 'rb')
  transfer.upload_file(sourcefile , bucket_name, '{}/{}'.format(folder, filename))
  
def removefile(sourcefile):
  os.remove(sourcefile)


def downloadfile(bucket_name, dst_folder, filepath):
  """
  @param bucket_name: S3 bucket name
  @param dst_folder: Folder to download file
  @param filepath: S3 Filepath
  """
#  client = boto3.client('s3',)
#  transfer = S3Transfer(client)
#  # Download s3://bucket/key to ./folder/myfile
#  transfer.download_file(bucket_name, filepath, '{}/{}'.format(dst_folder,filepath.split('/')[-1]))
  s3 = boto3.resource('s3')
  if not os.path.exists(dst_folder):
    os.mkdir(dst_folder)
  bucket = s3.Bucket(bucket_name)
  filename = filepath.split('/')[-1]
  with open('{}/{}'.format(dst_folder, filename), 'wb') as data:
    bucket.download_fileobj(filepath, data)


