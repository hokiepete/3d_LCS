clear all
close all
clc
load patches
len = length(out);
index = 1;
for i=2:len
  if size(out(i).faces,1) > 0
      large_lcs(index)=out(i);
      index = index+1;
  end
end
len=length(large_lcs);
figure
hold on
for i =1:len
    patch(large_lcs(i),'FaceColor','blue','EdgeColor','none');
end
axis([min(min(min(x))),max(max(max(x))),min(min(min(y))),max(max(max(y))),min(min(min(z))),max(max(max(z)))])
camlight 
lighting gouraud
xlabel('x (meters)')
ylabel('y (meters)')
zlabel('z (meters)')
%axis tight
view(3)
%}