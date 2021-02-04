# Test image similarity deployment with Postman

Follow these instructions to test you deployment with 
[Postman](https://www.postman.com/).

## 1. Deploy an experiment on the Peltarion Platform

Deploy an experiment on the [Peltarion Platform](https://platform.peltarion.com/).

## 2. Configure Postman
1. Download this repository to your computer.
2. Open Postman.
3. Import both json-files into Postman.
4. In the top-right corner, select the `Similarity Search` environment in the environment dropdown (from the start it says `No environment`).

## 3. Setup Postman with your deployment
1. Click the eye button next to the Environment-dropdown.
2. Click `Edit`.
3. Navigate to the Deployment view on the Peltarion Platform.
4. Copy the deployment `URL` and paste it into the `Current value` column and `deploymentID` row.
5. Copy the `Token` and paste it into the `Current value` column and `token` row.

## 4. Test your deployment with an image
1. Click `Collections` and then then POST `Image Similarity Search`.
2. Click the `Body` tab.
3. Select a local image to test your deployment to find similar images.
4. Click `Send` and wait....
5. Click the `Visualize` tab.