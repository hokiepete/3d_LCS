%close all

load grounddata
img = imread('Map.png');
hold on;
xImage = linspace(-38700, 38700,670);
yImage = linspace(38400, -38400,633);
[xImage,yImage]=meshgrid(xImage,yImage);
zImage = flipud(ground);%zeros(633,670);
surf(xImage,yImage,zImage,...    % Plot the surface
     'CData',img,...
     'FaceColor','texturemap','edgecolor','none');
%}
%zlim([min(min(ground)),8000]);