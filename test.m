%
clear all
close all
clc
%{
load thresh_lcs
out = splitFV(attFV);
save patches out x y z
%}
load patches
len = length(out);
index = 1;
%
for i=2:len
  if size(out(i).faces,1) > 500
      large_lcs(index)=out(i);
      index = index+1;
  end
end

%}
len=length(large_lcs);
hold on
for i =1:len
    figure
    patch(large_lcs(i),'FaceColor','blue','EdgeColor','none');
    axis([min(min(min(x))),max(max(max(x))),min(min(min(y))),max(max(max(y))),min(min(min(z))),max(max(max(z)))])
    camlight 
    lighting gouraud
    xlabel('x (meters)')
    ylabel('y (meters)')
    zlabel('z (meters)')
    %axis tight
    view(3)
end
%{
%patch(out(16),'FaceColor','blue','EdgeColor','none');
axis([min(min(min(x))),max(max(max(x))),min(min(min(y))),max(max(max(y))),min(min(min(z))),max(max(max(z)))])
camlight 
lighting gouraud
xlabel('x (meters)')
ylabel('y (meters)')
zlabel('z (meters)')
%axis tight
view(3)
%}