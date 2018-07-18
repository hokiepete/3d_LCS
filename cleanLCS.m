close all
clear all
clc
load FV


%{
xx = attFV.vertices(:,1);
yy = attFV.vertices(:,2);
zz = attFV.vertices(:,3);


%tri = delaunay(xx,yy,zz);
%trisurf(tri,xx,yy,zz,'edgecolor','none','FaceAlpha',0.3)
dt = delaunayTriangulation(xx,yy,zz);
maxdist=520*2;
%maxdist=300;
len=length(dt(:,1))

%L=dt.ConnectivityList(i,:);
a=dt.Points(dt.ConnectivityList(:,1),:);
b=dt.Points(dt.ConnectivityList(:,2),:);
c=dt.Points(dt.ConnectivityList(:,3),:);
d=dt.Points(dt.ConnectivityList(:,4),:);
distAB = sqrt((a(:,1)-b(:,1)).^2+(a(:,2)-b(:,2)).^2+(a(:,3)-b(:,3)).^2);
distAC = sqrt((a(:,1)-c(:,1)).^2+(a(:,2)-c(:,2)).^2+(a(:,3)-c(:,3)).^2);
distAD = sqrt((a(:,1)-d(:,1)).^2+(a(:,2)-d(:,2)).^2+(a(:,3)-d(:,3)).^2);
distBC = sqrt((b(:,1)-c(:,1)).^2+(b(:,2)-c(:,2)).^2+(b(:,3)-c(:,3)).^2);
distBD = sqrt((b(:,1)-d(:,1)).^2+(b(:,2)-d(:,2)).^2+(b(:,3)-d(:,3)).^2);
distCD = sqrt((c(:,1)-d(:,1)).^2+(c(:,2)-d(:,2)).^2+(c(:,3)-d(:,3)).^2);
disTest = [distAB < maxdist, distAC < maxdist ,distAD < maxdist,...
           distBC < maxdist, distBD < maxdist ,distCD < maxdist];
index =1;
for i = 1:len
    i
    if(min(disTest(i,:)))
        newConnectivity(index,:)=dt.ConnectivityList(i,:);
        index = index + 1
    end
end

save connenct newConnectivity dt

figure
%tetramesh(newConnectivity, newPoints, 'FaceColor', 'red')
tetramesh(newConnectivity, dt.Points, 'FaceColor', 'blue','edgecolor','none')
camlight
%shading interp
%}


