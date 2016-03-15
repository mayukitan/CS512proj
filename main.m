clc;
clear;

%{
%%
train = tdfread('training_all.txt', '\t');
truth = tdfread('ground_truth_all.txt', '\t');
%%
train_cell = cell(length(train.actor),4);
train_cell(:,1) = cellstr(train.repo_name);
train_cell(:,2) = cellstr(train.repo_owner);
train_cell(:,3) = cellstr(train.actor);
train_cell(:,4) = cellstr(train.language);

%%
truth_cell = cell(length(truth.actor),4);
truth_cell(:,1) = cellstr(truth.repo_name);
truth_cell(:,2) = cellstr(truth.repo_owner);
truth_cell(:,3) = cellstr(truth.actor);
truth_cell(:,4) = cellstr(truth.language);
%}


load('data.mat');
author_sort = sortrows(train_cell,3);
[uv,~,idx] = unique(author_sort(:,3));
n = accumarray(idx(:),1);
author_unq = [uv num2cell(n)];
author_unq_sort = sortrows(author_unq,-2);
author_tab = cell2table(author_unq_sort,'VariableNames',{'Author','Count'});
writetable(author_tab,'train_top_authors.txt','Delimiter','\t');
