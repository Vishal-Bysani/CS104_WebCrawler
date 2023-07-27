import argparse
import warnings
import requests
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

# Function to get file size
def get_file_size(url):
    try:
        response = requests.head(url)
        #checks whether the user wants the file size or not
        if args.size!='Y':
            return None
        else:
          if 'Content-Length' in response.headers:
              size = int(response.headers['Content-Length'])
              return size
          else:
              return None
    except:
        return None

# Function to crawl the website
def crawler(site, current_level, threshold):
    if threshold is not None and current_level > threshold:
        return

    link_list=[]    #Empty list to store the links obtained for the site in the current loop
    r = requests.get(site)
    s = BeautifulSoup(r.text, "lxml")
    href_tags = s.find_all(href=True)
    src_tags = s.find_all(src=True)

    #loop to make all the links obtained from href tags into valid urls
    for tag in href_tags:   
        href_value = tag['href']
        if not href_value.startswith("http"):
            if href_value.startswith("//"):
                href_value="http:"+href_value
            elif href_value.startswith("/"):
                href_value = site + href_value
            elif href_value.startswith('#'):
                continue
            else:
                href_value = site + '/' + href_value
        link_list.append(href_value)

    #loop to make all the links obtained from src tags into valid urls
    for tag in src_tags:
        src_value = tag['src']
        if not src_value.startswith("http"):
            if src_value.startswith("//"):
                src_value="http:"+src_value
            elif src_value.startswith("/"):
                src_value = site + src_value
            elif src_value.startswith('#'):
                continue
            else:
                src_value = site + '/' + src_value
        link_list.append(src_value)

    #in order to remove all the repeated links
    link_list = set(link_list)
    link_list = list(link_list)

    if current_level > len(files):
        files.append(0)
        internal_links.append({'HTML': {}, 'CSS': {}, 'JS': {}, 'JPG': {}, 'PNG' : {}, 'Others': {}})
        external_links.append({'HTML': {}, 'CSS': {}, 'JS': {}, 'JPG': {}, 'PNG' : {}, 'Others': {}})

    
    current_level += 1

    #segregation of links into HTML,CSS,JS,JPG,PNG and Others for both external and internal domain links. 
    for i in link_list:
        if i.startswith(original_site):
          if ".html" in i:
              internal_links[current_level-2]['HTML'][i] = get_file_size(i)
          elif ".css" in i:
              internal_links[current_level-2]['CSS'][i] = get_file_size(i)
          elif ".js" in i and "json" not in i:
              internal_links[current_level-2]['JS'][i] = get_file_size(i)
          elif ".jpg" in i:
              internal_links[current_level-2]['JPG'][i] = get_file_size(i)
          elif ".png" in i:
              internal_links[current_level-2]['PNG'][i]=get_file_size(i)
          else:
              internal_links[current_level-2]['Others'][i] = get_file_size(i)
          print(i)
          crawler(i, current_level ,threshold)    #This crawls only the internal domain links.


        else:
          if ".html" in i:
            external_links[current_level-2]['HTML'][i] = get_file_size(i)
          elif ".css" in i:
              external_links[current_level-2]['CSS'][i] = get_file_size(i)
          elif ".js" in i and "json" not in i:
              external_links[current_level-2]['JS'][i] = get_file_size(i)
          elif ".jpg" in i:
              external_links[current_level-2]['JPG'][i] = get_file_size(i)
          elif ".png" in i:
              external_links[current_level-2]['PNG'][i]=get_file_size(i)
          else:
              external_links[current_level-2]['Others'][i] = get_file_size(i)

        internal=len(internal_links[current_level-2]['HTML'])+len(internal_links[current_level-2]['CSS'])+len(internal_links[current_level-2]['JS'])+len(internal_links[current_level-2]['JPG'])+len(internal_links[current_level-2]['PNG'])+len(internal_links[current_level-2]['Others'])
        external=len(external_links[current_level-2]['HTML'])+len(external_links[current_level-2]['CSS'])+len(external_links[current_level-2]['JS'])+len(external_links[current_level-2]['JPG'])+len(external_links[current_level-2]['PNG'])+len(external_links[current_level-2]['Others'])

        files[current_level-2] = internal+external    #indicates the total number of files of each level which are crawled till now

        print(files)  #used to indicate the progress of the program
        
            






#to parse the command line arguments
parser = argparse.ArgumentParser(description='Web Crawler')
parser.add_argument('-u', '--url', required=True,type=str, help='URL of the website to crawl')
parser.add_argument('-t', '--threshold',required=False, type=int, help='Threshold (depth of recursion)')
parser.add_argument('-o', '--output',required=False,type=str, help='Output file')
parser.add_argument('-s','--size',required=False,type=str,help='To ask the user if he wants to find the files size')  #the code finds the file size as well if the user provides 'Y' as argument with s tag
args = parser.parse_args()


if args.threshold<=0 :
    raise ValueError("Invalid Threshold")

# Initialize variables
files = [0]
internal_links = [{'HTML': {}, 'CSS': {}, 'JS': {}, 'JPG': {}, 'PNG':{}, 'Others': {}}]
external_links = [{'HTML': {}, 'CSS': {}, 'JS': {}, 'JPG': {}, 'PNG':{}, 'Others': {}}]

# Crawl the website
original_site=args.url
crawler(original_site, 1, args.threshold)
output=args.output

if args.size=='Y': #When the user want the file sizes
  if output is None:
          # Print the output to terminal
          for i in range(len(files)):
              print(f'At recursion level: {i+1}\n')
              internal=len(internal_links[i]['HTML'])+len(internal_links[i]['CSS'])+len(internal_links[i]['JS'])+len(internal_links[i]['JPG'])+len(internal_links[i]['PNG'])+len(internal_links[i]['Others'])
              external=len(external_links[i]['HTML'])+len(external_links[i]['CSS'])+len(external_links[i]['JS'])+len(external_links[i]['JPG'])+len(external_links[i]['PNG'])+len(external_links[i]['Others'])

              print(f'Total number of files in this level: {files[i]}\n')
              print('Of these files, the various types are:')
              print(f'INTERNAL LINKS: {internal}\n\n')
              print(f'HTML: {len(internal_links[i]["HTML"])}')
              for j in internal_links[i]['HTML'].items():
                  print(j)
              print('\n')
              print(f'CSS: {len(internal_links[i]["CSS"])}')
              for j in internal_links[i]['CSS'].items():
                  print(j)
              print('\n')
              print(f'JavaScript: {len(internal_links[i]["JS"])}')
              for j in internal_links[i]['JS'].items():
                  print(j)
              print('\n')
              print(f'JPG: {len(internal_links[i]["JPG"])}')
              for j in internal_links[i]['JPG'].items():
                  print(j)
              print('\n')
              print(f'PNG: {len(internal_links[i]["PNG"])}')
              for j in internal_links[i]['PNG'].items():
                  print(j)
              print('\n')
              print(f'Others: {len(internal_links[i]["Others"])}\n\n')
              for j in internal_links[i]['Others'].items():
                  print(j)
              print('\n')

              print(f'EXTERNAL LINKS: {external}\n\n')
              print(f'HTML: {len(external_links[i]["HTML"])}')
              for j in external_links[i]['HTML'].items():
                  print(j)
              print('\n')
              print(f'CSS: {len(external_links[i]["CSS"])}')
              for j in external_links[i]['CSS'].items():
                  print(j)
              print('\n')
              print(f'JavaScript: {len(external_links[i]["JS"])}')
              for j in external_links[i]['JS'].items():
                  print(j)
              print('\n')
              print(f'JPG: {len(external_links[i]["JPG"])}')
              for j in external_links[i]['JPG'].items():
                  print(j)
              print('\n')
              print(f'PNG: {len(external_links[i]["PNG"])}')
              for j in external_links[i]['PNG'].items():
                  print(j)
              print('\n')
              print(f'Others: {len(external_links[i]["Others"])}\n\n')
              for j in external_links[i]['Others'].items():
                  print(j)
              print('\n')




  else:
              # Write the output to file
          with open(args.output, 'w') as f:
              for i in range(len(files)):
                  internal=len(internal_links[i]['HTML'])+len(internal_links[i]['CSS'])+len(internal_links[i]['JS'])+len(internal_links[i]['JPG'])+len(internal_links[i]['PNG'])+len(internal_links[i]['Others'])
                  external=len(external_links[i]['HTML'])+len(external_links[i]['CSS'])+len(external_links[i]['JS'])+len(external_links[i]['JPG'])+len(external_links[i]['PNG'])+len(external_links[i]['Others'])

                  f.write(f'At recursion level: {i+1}\n')
                  f.write(f'Total number of files in this level: {files[i]}\n')
                  f.write('Of these files, the various types are:\n')
                  f.write(f'INTERNAL LINKS: {internal}\n\n')
                  f.write(f'HTML: {len(internal_links[i]["HTML"])}\n')
                  for j in internal_links[i]['HTML'].items():
                      f.write(f'{str(j)}\n')
                  f.write('\n\n')
                  f.write(f'CSS: {len(internal_links[i]["CSS"])}\n')
                  for j in internal_links[i]['CSS'].items():
                      f.write(f'{str(j)}\n')
                  f.write('\n\n')
                  f.write(f'JavaScript: {len(internal_links[i]["JS"])}\n')
                  for j in internal_links[i]['JS'].items():
                      f.write(f'{str(j)}\n')
                  f.write('\n\n')
                  f.write(f'JPG: {len(internal_links[i]["JPG"])}\n')
                  for j in internal_links[i]['JPG'].items():
                      f.write(f'{str(j)}\n')
                  f.write('\n\n')
                  f.write(f'PNG: {len(internal_links[i]["PNG"])}\n')
                  for j in internal_links[i]['PNG'].items():
                      f.write(f'{str(j)}\n')
                  f.write(f'Others: {len(internal_links[i]["Others"])}\n\n')
                  for j in internal_links[i]['Others'].items():
                      f.write(f'{str(j)}\n')
                  f.write('\n')

                  f.write(f'EXTERNAL LINKS: {external}\n\n')
                  f.write(f'HTML: {len(external_links[i]["HTML"])}\n')
                  for j in external_links[i]['HTML'].items():
                      f.write(f'{str(j)}\n')
                  f.write('\n\n')
                  f.write(f'CSS: {len(external_links[i]["CSS"])}\n')
                  for j in external_links[i]['CSS'].items():
                      f.write(f'{str(j)}\n')
                  f.write('\n\n')
                  f.write(f'JavaScript: {len(external_links[i]["JS"])}\n')
                  for j in external_links[i]['JS'].items():
                      f.write(f'{str(j)}\n')
                  f.write('\n\n')
                  f.write(f'JPG: {len(external_links[i]["JPG"])}\n')
                  for j in external_links[i]['JPG'].items():
                      f.write(f'{str(j)}\n')
                  f.write('\n\n')
                  f.write(f'PNG: {len(external_links[i]["PNG"])}\n')
                  for j in external_links[i]['PNG'].items():
                      f.write(f'{str(j)}\n')
                  f.write(f'Others: {len(external_links[i]["Others"])}\n\n')
                  for j in external_links[i]['Others'].items():
                      f.write(f'{str(j)}\n')
                  f.write('\n')
                
else: #When the user does not want the file size
    if output is None:
          # Print the output to terminal
          for i in range(len(files)):
              print(f'At recursion level: {i+1}\n')
              internal=len(internal_links[i]['HTML'])+len(internal_links[i]['CSS'])+len(internal_links[i]['JS'])+len(internal_links[i]['JPG'])+len(internal_links[i]['PNG'])+len(internal_links[i]['Others'])
              external=len(external_links[i]['HTML'])+len(external_links[i]['CSS'])+len(external_links[i]['JS'])+len(external_links[i]['JPG'])+len(external_links[i]['PNG'])+len(external_links[i]['Others'])

              print(f'Total number of files in this level: {files[i]}\n')
              print('Of these files, the various types are:')
              print(f'INTERNAL LINKS: {internal}\n\n')
              print(f'HTML: {len(internal_links[i]["HTML"])}')
              for j in internal_links[i]['HTML'].items():
                  print(j[0])
              print('\n')
              print(f'CSS: {len(internal_links[i]["CSS"])}')
              for j in internal_links[i]['CSS'].items():
                  print(j[0])
              print('\n')
              print(f'JavaScript: {len(internal_links[i]["JS"])}')
              for j in internal_links[i]['JS'].items():
                  print(j[0])
              print('\n')
              print(f'JPG: {len(internal_links[i]["JPG"])}')
              for j in internal_links[i]['JPG'].items():
                  print(j[0])
              print('\n')
              print(f'PNG: {len(internal_links[i]["PNG"])}')
              for j in internal_links[i]['PNG'].items():
                  print(j[0])
              print('\n')
              print(f'Others: {len(internal_links[i]["Others"])}\n\n')
              for j in internal_links[i]['Others'].items():
                  print(j[0])
              print('\n')

              print(f'EXTERNAL LINKS: {external}\n\n')
              print(f'HTML: {len(external_links[i]["HTML"])}')
              for j in external_links[i]['HTML'].items():
                  print(j[0])
              print('\n')
              print(f'CSS: {len(external_links[i]["CSS"])}')
              for j in external_links[i]['CSS'].items():
                  print(j[0])
              print('\n')
              print(f'JavaScript: {len(external_links[i]["JS"])}')
              for j in external_links[i]['JS'].items():
                  print(j[0])
              print('\n')
              print(f'JPG: {len(external_links[i]["JPG"])}')
              for j in external_links[i]['JPG'].items():
                  print(j[0])
              print('\n')
              print(f'PNG: {len(external_links[i]["PNG"])}')
              for j in external_links[i]['PNG'].items():
                  print(j[0])
              print('\n')
              print(f'Others: {len(external_links[i]["Others"])}\n\n')
              for j in external_links[i]['Others'].items():
                  print(j[0])
              print('\n')




    else:
                # Write the output to file
            with open(args.output, 'w') as f:
                for i in range(len(files)):
                    internal=len(internal_links[i]['HTML'])+len(internal_links[i]['CSS'])+len(internal_links[i]['JS'])+len(internal_links[i]['JPG'])+len(internal_links[i]['PNG'])+len(internal_links[i]['Others'])
                    external=len(external_links[i]['HTML'])+len(external_links[i]['CSS'])+len(external_links[i]['JS'])+len(external_links[i]['JPG'])+len(external_links[i]['PNG'])+len(external_links[i]['Others'])

                    f.write(f'At recursion level: {i+1}\n')
                    f.write(f'Total number of files in this level: {files[i]}\n')
                    f.write('Of these files, the various types are:\n')
                    f.write(f'INTERNAL LINKS: {internal}\n\n')
                    f.write(f'HTML: {len(internal_links[i]["HTML"])}\n')
                    for j in internal_links[i]['HTML'].items():
                        f.write(f'{str(j[0])}\n')
                    f.write('\n\n')
                    f.write(f'CSS: {len(internal_links[i]["CSS"])}\n')
                    for j in internal_links[i]['CSS'].items():
                        f.write(f'{str(j[0])}\n')
                    f.write('\n\n')
                    f.write(f'JavaScript: {len(internal_links[i]["JS"])}\n')
                    for j in internal_links[i]['JS'].items():
                        f.write(f'{str(j[0])}\n')
                    f.write('\n\n')
                    f.write(f'JPG: {len(internal_links[i]["JPG"])}\n')
                    for j in internal_links[i]['JPG'].items():
                        f.write(f'{str(j[0])}\n')
                    f.write('\n\n')
                    f.write(f'PNG: {len(internal_links[i]["PNG"])}\n')
                    for j in internal_links[i]['PNG'].items():
                        f.write(f'{str(j[0])}\n')
                    f.write(f'Others: {len(internal_links[i]["Others"])}\n\n')
                    for j in internal_links[i]['Others'].items():
                        f.write(f'{str(j[0])}\n')
                    f.write('\n')

                    f.write(f'EXTERNAL LINKS: {external}\n\n')
                    f.write(f'HTML: {len(external_links[i]["HTML"])}\n')
                    for j in external_links[i]['HTML'].items():
                        f.write(f'{str(j[0])}\n')
                    f.write('\n\n')
                    f.write(f'CSS: {len(external_links[i]["CSS"])}\n')
                    for j in external_links[i]['CSS'].items():
                        f.write(f'{str(j[0])}\n')
                    f.write('\n\n')
                    f.write(f'JavaScript: {len(external_links[i]["JS"])}\n')
                    for j in external_links[i]['JS'].items():
                        f.write(f'{str(j[0])}\n')
                    f.write('\n\n')
                    f.write(f'JPG: {len(external_links[i]["JPG"])}\n')
                    for j in external_links[i]['JPG'].items():
                        f.write(f'{str(j[0])}\n')
                    f.write('\n\n')
                    f.write(f'PNG: {len(external_links[i]["PNG"])}\n')
                    for j in external_links[i]['PNG'].items():
                        f.write(f'{str(j[0])}\n')
                    f.write(f'Others: {len(external_links[i]["Others"])}\n\n')
                    for j in external_links[i]['Others'].items():
                        f.write(f'{str(j[0])}\n')
                    f.write('\n')
      
# Create subplots
fig, axs = plt.subplots(len(files), 2, figsize=(12, 6))
colors = {
    'HTML': 'red',
    'CSS': 'blue',
    'JS': 'green',
    'JPG': 'orange',
    'PNG': 'purple',
    'Others': 'gray'
}
# Iterate over data and plot
for i in range(len(files)):
    y1 = np.array([len(internal_links[i]['HTML']), len(internal_links[i]['CSS']), len(internal_links[i]['JS']), len(internal_links[i]['JPG']), len(internal_links[i]['PNG']), len(internal_links[i]['Others'])])
    y2 = np.array([len(external_links[i]['HTML']), len(external_links[i]['CSS']), len(external_links[i]['JS']), len(external_links[i]['JPG']), len(external_links[i]['PNG']), len(external_links[i]['Others'])])
    x = np.array(['HTML', 'CSS', 'JS', 'JPG', 'PNG', 'Others'])

    #to get the corresponding color for each file type
    file_color = [colors[file_type] for file_type in x]

    if len(files) == 1:
        axs[0].bar(x, y1, color=file_color)
        axs[1].bar(x, y2, color=file_color)
        axs[0].set_title(f"Recursion Level 1: Internal links")
        axs[1].set_title(f"Recursion Level 1: External links")
        axs[0].set_ylabel("Number of Files")
        axs[0].set_xlabel("File Types")
        axs[1].set_ylabel("Number of Files")
        axs[1].set_xlabel("File Types")

    else:
      axs[i][0].bar(x, y1, color=file_color)
      axs[i][1].bar(x, y2, color=file_color)
      axs[i][0].set_title(f"Recursion Level {i+1}: Internal links")
      axs[i][1].set_title(f"Recursion Level {i+1}: External links")
      axs[i][0].set_ylabel("Number of Files")
      axs[i][0].set_xlabel("File Types")
      axs[i][1].set_ylabel("Number of Files")
      axs[i][1].set_xlabel("File Types")

plt.tight_layout()  # Adjust the positions and spacing of subplots
plt.savefig("Files_Distribution.png")
plt.show()