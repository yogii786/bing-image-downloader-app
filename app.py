import os
import shutil
import streamlit as st
from zipfile import ZipFile
from bing_image_downloader import downloader


def get_all_file_paths(directory):
    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # returning all file paths
    return file_paths


def zipfile(search_term):
    # path to folder which needs to be zipped
    directory = './' + search_term

    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)

    # printing the list of all files to be zipped
    for file_name in file_paths:
        print(file_name)

    # writing files to a zipfile
    with ZipFile(search_term + '.zip', 'w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)
    print("Zip file created !")


def main():
    st.header("Bing Image Downloader App")  # app header
    st.text("Build with streamlit and bing_image_downloader")
    st.subheader("Search Image")  # app subheader

    # Getting the search term and limit count from user
    # using text_input and number_input to download images
    search_text = st.text_input("Search Term : ",)
    limit_number = st.number_input(
        "No of Images to Download: ", min_value=1, max_value=50)  # limit ranges from 1 to 50 if user gives above 50 app only takes 50 as the limit

    # if user clicks the Search button
    if st.button("Search"):
        # if search term is empty then displays the warning message
        if search_text == '':
            st.warning('Please, Enter the Search Term to Continue!')

        # if search text is not empty
        else:
            # if the search term folder already exists then remove the folder
            if os.path.isdir(search_text):
                shutil.rmtree(search_text)

            # To indicate the download as been started
            st.info('Downloading...')

            # Search for the images, Download it and store it in a folder named same as the search term
            downloader.download(query=search_text, limit=limit_number, output_dir=search_text,
                                adult_filter_off=True, force_replace=False, timeout=60, verbose=True)

            zipfile(search_text)  # calling zipfile() to zip the folder
            file_name = search_text + '.zip'
            st.info('Click on the Download button to download the zip file 👇')

            # Then by clicking download zip button user can download the images zip file
            with open(file_name, "rb") as fp:
                button = st.download_button(
                    label="Download",
                    data=fp,
                    file_name=file_name,
                    mime="application/zip"
                )


if __name__ == "__main__":
    main()  # calling main() to execute first
