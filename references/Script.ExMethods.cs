public ImageData MatToImageData(Mat matImage)
{
    ImageData imgOut = new ImageData();
    byte[] buffer = new Byte[matImage.Width * matImage.Height * matImage.Channels()];
    Marshal.Copy(matImage.Ptr(0), buffer, 0, buffer.Length);

    if (1 == matImage.Channels())
    {
        imgOut.Buffer = buffer;
        imgOut.Width = matImage.Width;
        imgOut.Height = matImage.Height;
        imgOut.PixelFormat = ImagePixelFormate.MONO8;
    }
    else if (3 == matImage.Channels())
    {
        //交换R与B通道
        for (int i = 0; i < buffer.Length - 2; i += 3)
        {
            byte temp = buffer[i];
            buffer[i] = buffer[i + 2];
            buffer[i + 2] = temp;
        }
        imgOut.Buffer = buffer;
        imgOut.Width = matImage.Width;
        imgOut.Height = matImage.Height;
        imgOut.PixelFormat = ImagePixelFormate.RGB24;
    }
    return imgOut;
}

public Mat ImageDataToMat(ImageData img)
{
    Mat matImage = new Mat();
    if (ImagePixelFormate.MONO8 == img.PixelFormat)
    {
        matImage = Mat.Zeros(img.Height, img.Width, MatType.CV_8UC1);
        IntPtr grayPtr = Marshal.AllocHGlobal(img.Width * img.Height);
        Marshal.Copy(img.Buffer, 0, matImage.Ptr(0), img.Buffer.Length);
        //用完记得释放指针
        Marshal.FreeHGlobal(grayPtr);
    }
    else if (ImagePixelFormate.RGB24 == img.PixelFormat)
    {
        matImage = Mat.Zeros(img.Height, img.Width, MatType.CV_8UC3);
        IntPtr rgbPtr = Marshal.AllocHGlobal(img.Width * img.Height * 3);
        Marshal.Copy(img.Buffer, 0, matImage.Ptr(0), img.Buffer.Length);
        Cv2.CvtColor(matImage, matImage, ColorConversionCodes.RGB2BGR);
        //用完记得释放指针
        Marshal.FreeHGlobal(rgbPtr);
    }
    return matImage;
}