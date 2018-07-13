
close all;
clear all
clc
sigmatol=1.1
concavitytol=0
load ftle
ftle = f(:,1:4:end,:);
eig1 = f(:,2:4:end,:);
eig2 = f(:,3:4:end,:);
eig3 = f(:,4:4:end,:);
clear f
dim = size(ftle);
hx=300
hy=300
hz=200
%pr = prctile(reshape(ftle,1,[]),95)
ftle_ordered = sort(reshape(ftle,1,[]));
index = ceil((length(ftle_ordered)*0.98));
pr = ftle_ordered(index)
[dx,dy,dz] = gradient(ftle,hx,hy,hz);
[dxdx,dydx,dzdx] = gradient(dx,hx,hy,hz);
[dxdy,dydy,dzdy] = gradient(dy,hx,hy,hz);
[dxdz,dydz,dzdz] = gradient(dz,hx,hy,hz);

stat = reshape(ftle,[],1);
s = std(stat) ;
fmean = mean(stat);

'begin formating'
for i = 1:dim(1)
    for j = 1:dim(2)
        for k = 1:dim(3)
            H = [dxdx(i,j,k),dxdy(i,j,k),dxdz(i,j,k);dydx(i,j,k),dydy(i,j,k),dydz(i,j,k);dzdx(i,j,k),dzdy(i,j,k),dzdz(i,j,k)];
            derivative = [dx(i,j,k);dy(i,j,k);dz(i,j,k)];
            Cvec = [eig1(i,j,k),eig2(i,j,k),eig3(i,j,k)]';
            concavity(i,j,k) = dot((H*Cvec),Cvec);
            Cdiv(i,j,k) = dot(derivative,Cvec);
            %{
            if or(concavity(i,j,k)>=concavitytol,ftle(i,j,k)<(fmean+sigmatol*s))
                Cdiv(i,j,k) = nan;
            else
                Cdiv(i,j,k) = dot(derivative,Cvec);
            end
            %}
        end
    end
end
clear H eig1 eig2 eig3 Cvec dx dy dz dxdx dxdy dxdz dydx dydy dydz dzdx dzdy dzdz i j k derivative
%clear ftle


%dirdiv = dx.*eig1 + dy.*eig2 + dz.*eig3;
%clear dx dy dz eig1 eig2 eig3
x = linspace(-38700,38700,259);
y = linspace(-38400,38400,257);
z= linspace(0,8000,41);
[x,y,z]=meshgrid(x,y,z);
'isosurface'
FV=isosurface(x,y,z,Cdiv,0);
%{
[faces,verts,colors]
FV.vertices = vertices
FV.faces = faces;

figure(2)
p=patch(FV);
set(p,'FaceColor','blue','EdgeColor','none');
camlight 
lighting gouraud
xlabel('x (meters)')
ylabel('y (meters)')
zlabel('z (meters)')
view(3)

%}
vertcon = interp3(x,y,z,concavity,FV.vertices(:,1),FV.vertices(:,2),FV.vertices(:,3),'spline');
clear concavity
%
if ~isnan(sigmatol);
    stat = reshape(ftle,[],1);
    s = std(stat) ;
    fmean = mean(stat);
    threshhold = fmean+sigmatol*s
    ftle = interp3(x,y,z,ftle,FV.vertices(:,1),FV.vertices(:,2),FV.vertices(:,3),'spline');
    index = 1;
    'remove vertices'
    for i = 1:length(vertcon)
        %if or(vertcon(i)>=concavitytol,ftle(i)<(fmean+sigmatol*s))
         if or(vertcon(i)>=concavitytol,ftle(i)<pr)
            verticesToRemove(index) =  i;
            index = index + 1;
        end
    end
else
    index = 1;
    for i = 1:length(vertcon)
        if or(vertcon(i)>=concavitytol,ftle(i)<0)
            verticesToRemove(index) =  i;
            index = index + 1;
        end
    end
end
clear ftle vertconcavity index i


% Remove the vertex values at the specified index values
newVertices = FV.vertices;
newVertices(verticesToRemove,:) = [];

% Find the new index for each of the new vertices
[~, newVertexIndex] = ismember(FV.vertices, newVertices, 'rows');

% Find any faces that used the vertices that we removed and remove them
newFaces = FV.faces(all(~ismember(FV.faces, verticesToRemove), 2),:);

% Now updata the vertex indices to the new ones
newFaces = newVertexIndex(newFaces);

FV.vertices = newVertices;
FV.faces = newFaces;

attFV = FV;
clear FV newFaces newVertices verticesToRemove newVertexIndex newVertexIndex


figure
p=patch(attFV);
set(p,'FaceColor','blue','EdgeColor','none');
%set(p,'FaceColor','interp','EdgeColor','interp');
camlight 
lighting gouraud
xlabel('x (meters)')
ylabel('y (meters)')
zlabel('z (meters)')
axis tight
view(3)
%}
%{
[xSphere,ySphere,zSphere] = sphere(16);          % Points on a sphere
scatter3(xSphere(:),ySphere(:),zSphere(:),'.');  % Plot the points
axis equal;   % Make the axes scales match
hold on;      % Add to the plot
xlabel('x');
ylabel('y');
zlabel('z');
img = imread('map.png');     % Load a sample image
%xImage = [-0.5 0.5; -0.5 0.5];   % The x data for the image corners
%yImage = [0 0; 0 0];             % The y data for the image corners
%zImage = [0.5 0.5; -0.5 -0.5];   % The z data for the image corners
%}
img = imread('Map.png');
hold on;
xImage = [-38700 38700; -38700 38700];
yImage = [38400 38400; -38400 -38400];
zImage = [0 0; 0 0];
surf(xImage,yImage,zImage,...    % Plot the surface
     'CData',img,...
     'FaceColor','texturemap');
%{
model.cdata = dirdiv;
model.alpha = [];
model.xdata = [-38700,38700];
model.ydata = [-38400,38400];
model.zdata = [0,8000];
model.parent = [];
model.handles = [];
model.texture = '3D';
colormap(parula);
vol3d_v2(model);
xlabel('m E/W')
ylabel('m N/S')
zlabel('m alt')
%vol3d_v2('cdata',ftle(:,:,:,1))
view(3)
%caxis([0,cmax])
colorbar
%}