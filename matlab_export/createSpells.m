function [t] = createSpells(id, timeseries,key)
spells = [];
t = min(find(timeseries)); % BUG: currently does not output a spell for val=0
while t < length(timeseries)
    nextStart = min(find(timeseries(t:end)))+t-1; % same bug here (val0 bug)
    if length(nextStart) == 0
        break;
    end
    nextEnd = min(find([timeseries(nextStart) ~= timeseries(nextStart+1:end), 1]));
    spells(end+1,:) = [(nextStart) (nextEnd+nextStart-1), timeseries(nextStart)];
    t = nextStart + nextEnd;
end
id = repmat(id,size(spells,1),1);
if size(id,2) == 2
    source = id(:,1);
    target = id(:,2);
    t = table(source,target);
else
    t = table(id);
end

start = spells(:,1);
End = spells(:,2);
if(nargin > 2)
    key = repmat(cellstr(key),size(spells,1),1);
    values = (num2cell(spells(:,3)));
else
    key = repmat(cellstr(''),size(spells,1),1);
    values = repmat(cellstr(''),size(spells,1),1);
end
t = [t table(start, End)];% somehow change this to lowercase end
t = [t table(key,values)]; 
end