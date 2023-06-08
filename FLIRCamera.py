import PySpin

class FLIRCamera:
    
    def __init__(self):
        print("Setting up camera..")
        self.system = PySpin.System.GetInstance()
        self.cam_list = self.system.GetCameras()
        self.cam = None
    
    def begin(self):
        if self.cam_list.GetSize() == 0:
            self.cam_list.Clear()
            self.system.ReleaseInstance()
            return False
        else:
            self.cam = self.cam_list[0]
            self.nodemap_tldevice = self.cam.GetTLDeviceNodeMap()
            self.cam.Init()
            self.nodemap = self.cam.GetNodeMap()
            self.sNodemap = self.cam.GetTLStreamNodeMap()
            
            # Change bufferhandling mode to NewestOnly
            node_bufferhandling_mode = PySpin.CEnumerationPtr(self.sNodemap.GetNode('StreamBufferHandlingMode'))
            if not PySpin.IsReadable(node_bufferhandling_mode) or not PySpin.IsWritable(node_bufferhandling_mode):
                print('Unable to set stream buffer handling mode.. Aborting...')
                return False

            # Retrieve entry node from enumeration node
            node_newestonly = node_bufferhandling_mode.GetEntryByName('NewestOnly')
            if not PySpin.IsReadable(node_newestonly):
                print('Unable to set stream buffer handling mode.. Aborting...')
                return False

            # Retrieve integer value from entry node
            node_newestonly_mode = node_newestonly.GetValue()

            # Set integer value from entry node as new value of enumeration node
            node_bufferhandling_mode.SetIntValue(node_newestonly_mode)
            try:
                node_acquisition_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('AcquisitionMode'))
                if not PySpin.IsReadable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
                    print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...')
                    return False

                # Retrieve entry node from enumeration node
                node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
                if not PySpin.IsReadable(node_acquisition_mode_continuous):
                    print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
                    return False

                # Retrieve integer value from entry node
                acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()

                # Set integer value from entry node as new value of enumeration node
                node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
                
                self.cam.BeginAcquisition()
                
                device_serial_number = ''
                node_device_serial_number = PySpin.CStringPtr(self.nodemap_tldevice.GetNode('DeviceSerialNumber'))
                if PySpin.IsReadable(node_device_serial_number):
                    device_serial_number = node_device_serial_number.GetValue()
                    print('Device serial number retrieved as %s...' % device_serial_number)
            
            except PySpin.SpinnakerException as ex:
                print('Error: %s' % ex)
                return False
        return True
            
    def close(self):
        if self.cam != None:
            self.cam.EndAcquisition()
            self.cam.DeInit()
            del self.cam
            self.cam_list.Clear()
            self.system.ReleaseInstance()
        
    def getFrame(self):
        image_data = None
        try:
            self.image_result = self.cam.GetNextImage(1000)
            image_data = self.image_result.GetNDArray()
        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False
        return image_data
    
    def releaseFrame(self):
        self.image_result.Release()
