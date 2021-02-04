# Test image similarity deployment with Postman

Follow these instructions to test you deployment with 
[Postman](https://www.postman.com/).

## 1. Deploy an experiment on the Peltarion Platform

Deploy an experiment on the [Peltarion Platform](https://platform.peltarion.com/).

## 2. Configure Postman
1. Download this repository to your computer.
2. Open the Postman app.
3. Import both json-files into Postman.
4. In the top-right corner, select the `Similarity Search` environment in the Environment-dropdown (from the start it says `No environment`).

## 3. Manage environment
1. Click the eye button next to the Environment-dropdown.
2. Click `Edit` to open the _Manage environments_ window.
3. In separate window, navigate to the _Deployment view_ on the Peltarion Platform.
4. Copy the environment variables from the _Deployment view_ to the _CURRENT VALUE_ column in the _Manage environments_ window. 

![Environment Variables](img:EnvironmentVariables_PA1.png) 
- Copy the host address from the `URL` to the `similarySearchHost` field.
- Copy the deployment ID from end of the `URL` to the `deploymentID` field.
- Copy the `Token` to the `token` field.

## 4. Test your deployment with an image
1. Click `Collections` and then then POST `Image Similarity Search`.
2. Click the `Body` tab.
3. Select a local image to test your deployment to find similar images.
4. Click `Send` and wait....
5. Click the `Visualize` tab.