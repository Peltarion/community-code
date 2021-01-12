This is what needs to be done to finish the config off:

1. Update the hostname that will be used for production. Currently it is set to staging.
2. Update the HTML/CSS for displaying the similarity results to make it look more professional/pretty. Make sure you save (ctrl + s) and then export the config. The exported JSON config will be what you distribute. Wise to re-import it to ensure yours changes are there.

To use:
1. Import both files in to Postman
2. Select the `Similarity Search` environment in the environment dropdown (top-right)
3. Edit the environment config (the eye button next to the above dropdown) and set the `Current Value` column on `deploymentId` and `token`
4. Open `Image Similarity Search` request
5. Under the body tab, select the image you want to search for similar images for
6. Click `Send`
7. Click the `Visualize` tab