function [BW,maskedRGBImage] = createMask(RGB, rmin,rmax, gmin,gmax, bmin,bmax) 
    % Define thresholds for Red
    channel1Min = rmin;
    channel1Max = rmax;
    % Define thresholds for Green
    channel2Min = gmin;
    channel2Max = gmax;
    % Define thresholds for Blue
    channel3Min = bmin;
    channel3Max = bmax;
    % Create mask based on chosen histogram thresholds
    BW = ( (RGB(:,:,1) >= channel1Min) | (RGB(:,:,1) <= channel1Max) ) & ...
        (RGB(:,:,2) >= channel2Min ) & (RGB(:,:,2) <= channel2Max) & ...
        (RGB(:,:,3) >= channel3Min ) & (RGB(:,:,3) <= channel3Max);
    % Initialize output masked image based on input image.
    maskedRGBImage = RGB;
    % Set background pixels where BW is false to zero.
    maskedRGBImage(repmat(~BW,[1 1 3])) = 0;