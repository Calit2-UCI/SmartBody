# Set initial lighting for scene and parameters to fit character
viewer = getViewer()
viewer.show()

sscale = 1.0/scene.getScale()

camera = getCamera()
camera.setEye(0*sscale, 1.66*sscale, 1.85*sscale)
camera.setCenter(0, .92*sscale, 0)
camera.setFarPlane(100*sscale)
camera.setNearPlane(0.1*sscale)

cameraPawn = scene.createPawn("camera")
cameraPos = SrVec(0, 1.66*sscale, 1.85*sscale)
cameraPawn.setPosition(cameraPos)

light0 = scene.createPawn("light0")
light0Pos = SrVec(1.00*sscale, 2.50*sscale, 4.00*sscale)
light0.setPosition(light0Pos)
light0.setHPR(SrVec(157.479, 49.2828, -156.542))      #rotY, rotX, rotZ

light0.createBoolAttribute("lightCastShadow", True, True, "LightAttributes", 8, False, False, False, "Does the light cast shadow")
light0.createBoolAttribute("lightIsDirectional", True, True, "LightAttributes", 5, False, False, False, "Is the light a directional light")
light0.createVec3Attribute("lightDiffuseColor", 1, 1, 1, True, "LightAttributes", 10, False, False, False, "Diffuse color")
light0.createVec3Attribute("lightAmbientColor", 0, 0, 0, True, "LightAttributes", 20, False, False, False, "Ambient color")
light0.createVec3Attribute("lightSpecularColor", 0, 0, 0,  True, "LightAttributes", 30, False, False, False, "Specular color")
light0.createDoubleAttribute("lightSpotExponent", 0, True, "LightAttributes", 40, False, False, False, "Spotlight exponent")
light0.createVec3Attribute("lightSpotDirection", 0, 0, -1,  True, "LightAttributes", 50, False, False, False, "Spotlight direction")
light0.createDoubleAttribute("lightSpotCutoff", 180.0, True, "LightAttributes", 60, False, False, False, "Spotlight cutoff angle")
light0.createDoubleAttribute("lightConstantAttenuation", 1.0, True, "LightAttributes", 70, False, False, False, "Constant attenuation")
light0.createDoubleAttribute("lightLinearAttenuation", 0.0, True, "LightAttributes", 80, False, False, False, "Linear attenuation")
light0.createDoubleAttribute("lightQuadraticAttenuation", 0.0, True, "LightAttributes", 90, False, False, False, "Quadratic attenuation")


light1 = scene.createPawn("light1")
light1Pos = SrVec(1.00*sscale, 2.50*sscale, 4.00*sscale)
light1.setPosition(light1Pos)
light1.setHPR(SrVec(106.068, -54.7715, -105.279))

light1.createBoolAttribute("lightCastShadow", True, True, "LightAttributes", 8, False, False, False, "Does the light cast shadow")
light1.createBoolAttribute("lightIsDirectional", True, True, "LightAttributes", 5, False, False, False, "Is the light a directional light")
light1.createVec3Attribute("lightDiffuseColor", 1, 1, 1, True, "LightAttributes", 10, False, False, False, "Diffuse color")
light1.createVec3Attribute("lightAmbientColor", 0, 0, 0, True, "LightAttributes", 20, False, False, False, "Ambient color")
light1.createVec3Attribute("lightSpecularColor", 0, 0, 0,  True, "LightAttributes", 30, False, False, False, "Specular color")
light1.createDoubleAttribute("lightSpotExponent", 0, True, "LightAttributes", 40, False, False, False, "Spotlight exponent")
light1.createVec3Attribute("lightSpotDirection", 0, 0, -1,  True, "LightAttributes", 50, False, False, False, "Spotlight direction")
light1.createDoubleAttribute("lightSpotCutoff", 180.0, True, "LightAttributes", 60, False, False, False, "Spotlight cutoff angle")
light1.createDoubleAttribute("lightConstantAttenuation", 1.0, True, "LightAttributes", 70, False, False, False, "Constant attenuation")
light1.createDoubleAttribute("lightLinearAttenuation", 0.0, True, "LightAttributes", 80, False, False, False, "Linear attenuation")
light1.createDoubleAttribute("lightQuadraticAttenuation", 0.0, True, "LightAttributes", 90, False, False, False, "Quadratic attenuation")


light2 = scene.createPawn("light2")
light2Pos = SrVec(1.00*sscale, 2.50*sscale, 4.00*sscale)
light2.setPosition(light2Pos)
light2.setHPR(SrVec(179.825, -34.4736, 175.913))

light2.createBoolAttribute("lightCastShadow", True, True, "LightAttributes", 8, False, False, False, "Does the light cast shadow")
light2.createBoolAttribute("lightIsDirectional", True, True, "LightAttributes", 5, False, False, False, "Is the light a directional light")
light2.createVec3Attribute("lightDiffuseColor", 1, 1, 1, True, "LightAttributes", 10, False, False, False, "Diffuse color")
light2.createVec3Attribute("lightAmbientColor", 0, 0, 0, True, "LightAttributes", 20, False, False, False, "Ambient color")
light2.createVec3Attribute("lightSpecularColor", 0, 0, 0,  True, "LightAttributes", 30, False, False, False, "Specular color")
light2.createDoubleAttribute("lightSpotExponent", 0, True, "LightAttributes", 40, False, False, False, "Spotlight exponent")
light2.createVec3Attribute("lightSpotDirection", 0, 0, -1,  True, "LightAttributes", 50, False, False, False, "Spotlight direction")
light2.createDoubleAttribute("lightSpotCutoff", 180.0, True, "LightAttributes", 60, False, False, False, "Spotlight cutoff angle")
light2.createDoubleAttribute("lightConstantAttenuation", 1.0, True, "LightAttributes", 70, False, False, False, "Constant attenuation")
light2.createDoubleAttribute("lightLinearAttenuation", 0.0, True, "LightAttributes", 80, False, False, False, "Linear attenuation")
light2.createDoubleAttribute("lightQuadraticAttenuation", 0.0, True, "LightAttributes", 90, False, False, False, "Quadratic attenuation")
