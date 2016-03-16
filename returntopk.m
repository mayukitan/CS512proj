%% Function return top k entities from data
%% Variable i: Column to choose attribute
%%          data_cell: Data train/test in cell format
%% Return type: Table [entity count]
%% 
function topk_tab = returntopk(k, i, data_cell, attribute)

sorted= sortrows(data_cell,3);
[uv,~,idx] = unique(sorted(:,i));
n = accumarray(idx(:),1);
sorted_unq = [uv num2cell(n)];
sort_unq = sortrows(sorted_unq,-2);
% Pick top k results
topk_tab = cell2table(sort_unq(1:k,:),'VariableNames',{attribute,'Count'});
