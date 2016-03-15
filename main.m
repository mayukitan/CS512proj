clc;
clear;
%%
data = tdfread('ground_truth_py.txt', '\t');
%%
data_cell = cell(length(data.actor),4);
data_cell(:,1) = mat2cell(data.actor);
data_cell(:,2) = mat2cell(data.repo_name);
data_cell(:,3) = mat2cell(data.repo_owner);
data_cell(:,4) = mat2cell(data.language);

%%
actor_lst = unique(data(:,1));