from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import urllib
import requests
client_credentials_manager = SpotifyClientCredentials(client_id = 'd5d54db44c1a45a1a9d3ee4b588f778b', client_secret='ee8dedacd4334fb0a2b6cdc57af2d2d3')
from PIL import Image
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False
from io import BytesIO

playlistID = input("Enter Playlist Link: ")
playlistID = playlistID[len('playlist/') + playlistID.find('playlist/'): ]
print(playlistID)

userID = input("Enter Link to Playlist User: ")
userID = userID[len('user/') + userID.find('user/'): ]
print(userID)

def merge_images_row(image1, image2):
    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_width = width1 + width2
    result_height = max(height1, height2)

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))
    return result

def merge_images_col(image1, image2):
    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_height = height1 + height2
    result_width = max(width1, width2)

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(0, height1))
    return result


# Get Image URLs
play = sp.user_playlist(userID, playlistID)
albumurlset = set()
for i in play['tracks']['items']:
    albumurlset.add(i['track']['album']['images'][0]['url'])

print('Number Of Images Possible: ' + str(len(albumurlset)))

# Input Variables of the Code
rows = int(input('Enter Row Size: '))
cols = int(input('Enter Column Size: '))
outputname = input('Enter output file name: ') + '.jpg'

print('Generating Image of Size: ' + str(rows*cols))
if(len(albumurlset) < rows*cols):
    print('Not enough album art to generate output image. Please reduce row/column size.')
    exit(0)

rowImages = []
albumurlset = list(albumurlset)

imagecount = 0
for i in range(0,rows):
    rowImage = Image.new('RGB', (0,0))
    for j in range(0, cols):
        response = requests.get(albumurlset[imagecount])
        img = Image.open(BytesIO(response.content))
        rowImage = merge_images_row(rowImage, img)
        print(str((imagecount/(rows*cols))*100) + '%')
        imagecount+=1
    rowImages.append(rowImage)

finalImage = Image.new('RGB', (0,0))
for i in rowImages:
    finalImage = merge_images_col(finalImage, i)

finalImage.show()
finalImage.save(outputname)