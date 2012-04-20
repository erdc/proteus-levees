from proteus.default_so import *
pnList = [("re_gl_5_3d_p" , 
           "re_gl_5_3d_n"),
          ("sm_gl_5_3d_p" , 
           "sm_gl_5_3d_n")]

name = "gl_5_3d"
tnList=[float(i) for i in range(20)]
systemStepControllerType = Sequential_FixedStep
useOneArchive = True
archiveFlag = ArchiveFlags.EVERY_USER_STEP
