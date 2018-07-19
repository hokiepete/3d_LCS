clear all
close all
clc
load LCS_data
load rawisosurface
ftle_ordered = sort(reshape(ftle,1,[]));
index = floor((length(ftle_ordered)*0.9));
ftle_thresh = ftle_ordered(index)


vertcon = interp3(x,y,z,concavity,FV.vertices(:,1),FV.vertices(:,2),FV.vertices(:,3),'spline');
ftle = interp3(x,y,z,ftle,FV.vertices(:,1),FV.vertices(:,2),FV.vertices(:,3),'spline');
clear concavity

if ~isnan(ftle_thresh);
    index = 1;
    'remove vertices'
    for i = 1:length(vertcon)
         if or(vertcon(i)>=0,ftle(i)<ftle_thresh)
            verticesToRemove(index) =  i;
            index = index + 1;
        end
    end
else
    index = 1;
    for i = 1:length(vertcon)
        if or(vertcon(i)>=0,ftle(i)<0)
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

save thresh_lcs attFV x y z

figure
patch(attFV,'FaceColor','blue','EdgeColor','none');
camlight 
lighting gouraud
xlabel('x (meters)')
ylabel('y (meters)')
zlabel('z (meters)')
axis tight
view(3)