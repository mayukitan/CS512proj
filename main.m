clc;
clear;

%{
%% Read data
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
%% Pick subset of data
% Pick top 10000 authors to train
k = 10000;
train_author_tab = returntopk(k, 3, train_cell, 'Author');
train_repo_tab = returntopk(k, 1, train_cell, 'Repository');

[index, ~] = cellfun(@(x) ismember(x,train_author_tab.Author), train_cell(:,3), 'UniformOutput', 0);
train_cell_top = train_cell(cell2mat(index),:);
train_author_top = cell2table(train_cell_top,'VariableNames',{'repo_name' 'repo_owner' 'actor' 'language'});
writetable(train_author_top,'train_top_author.txt','Delimiter','\t');
%%
% Pick top 50 authors to test
k = 50;
test_author_tab = returntopk(k, 3, truth_cell, 'Author');
%writetable(test_author_tab ,'test_top_authors.txt','Delimiter','\t');

%% Check if all authors in test appear in train
%% If do not exist, remove from test data
flag_exist = zeros(size(test_author_tab,1),1);
flag_exist = cellfun(@(x) ismember(x,train_author_tab.Author), test_author_tab.Author(:,1),...
                 'UniformOutput', 0);












