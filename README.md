# DreamPainter-VR
DreamPainter allows users to view real-life landscape photospheres and, using the Gear VR's controls, toggle through the various stylized versions of those photospheres.

What it does:
  DreamPainter allows users to view real-life landscape photospheres and, using the Gear VR's controls, toggle through the various stylized versions of those photospheres. In an experimental mode, users can also "paint" the style of multiple artists onto the landscape photosphere with a virtual "brush", so they can mix and match multiple styles on the same sphere!
Example styles below: (http://i.imgur.com/wiOtLFY.jpg)

How we built it
  We used Logan Engstrom's fast style transfer neural network implementation found here to give a set of equirectangular photosphere images in the style of famous paintings such as Picabia's Udnie, The Great Wave off Kanagawa, Picasso's A Muse, and many more.
  Because we had limited computational power, we could not run an entire image through the neural net implementation at once, so we wrote an image processing pipeline that would slice each image into pieces, feed each one through the NN, and then stitch the results back together.
  We then used the Unity engine to transform the original and stylized photospheres into textures, and overlaid them onto a virtual sphere to create the viewing environment for our Samsung Gear VR app. We interfaced with the Gear VR's button controls to allow users to swipe to change their original image, and tap to toggle through each image's style.
  For the paintbrush feature, we used Unity's Gyroscope readings to obtain quaternion readings of the user's headset orientation. We then translated those readings into Euler angles, then used equirectangular projection mappings to align our angles with corresponding areas on the original 2-D image. This allowed the user to look at an area in the photo sphere, modify the 2-D painting, and have Unity remap the affected area into the sphere.
