clc;
clear;

%{
%%
train = tdfread('./Data/train.json', ',');
truth = tdfread('./Data/test.json', ',');

train_cell = cell(length(train.actor),4);
train_cell(:,1) = cellstr(train.repository_name);
train_cell(:,2) = cellstr(train.repository_owner);
train_cell(:,3) = cellstr(train.actor);
train_cell(:,4) = cellstr(train.repository_language);


truth_cell = cell(length(truth.actor),4);
truth_cell(:,1) = cellstr(truth.repository_name);
truth_cell(:,2) = cellstr(truth.repository_owner);
truth_cell(:,3) = cellstr(truth.actor);
truth_cell(:,4) = cellstr(truth.repository_language);
%}

%%
load('data.mat');
train_author_sort = sortrows(train_cell,3);
[uv,~,idx] = unique(train_author_sort(:,3));
n = accumarray(idx(:),1);
train_author_unq = [uv num2cell(n)];
train_author_unq_sort = sortrows(train_author_unq,-2);
% Pick top 10,000 authors
k = 10000;
train_author_tab = cell2table(train_author_unq_sort(1:k,:),'VariableNames',{'Author','Count'});
%writetable(author_tab,'train_top_authors.txt','Delimiter','\t');

test_author_sort = sortrows(truth_cell,3);
[uv,~,idx] = unique(test_author_sort(:,3));
n = accumarray(idx(:),1);
test_author_unq = [uv num2cell(n)];
test_author_unq_sort = sortrows(test_author_unq,-2);
% Pick top 50 authors to test
k = 50;
test_author_tab = cell2table(test_author_unq_sort(1:k,:),'VariableNames',{'Author','Count'});
%writetable(author_tab,'train_top_authors.txt','Delimiter','\t');

