try; cd(fileparts(mfilename('fullpath')));catch; end;
try;
   run ../../matlab/utilities/initPaths.m
catch
   msgbox({'Please change to the directory where this file is saved before running the rest of this code'},'Change directory'); 
end

buffhost='localhost';buffport=1972;
% wait for the buffer to return valid header information
hdr=[];
while ( isempty(hdr) || ~isstruct(hdr) || (hdr.nchans==0) ) % wait for the buffer to contain valid data
  try 
    hdr=buffer('get_hdr',[],buffhost,buffport); 
  catch
    hdr=[];
    fprintf('Invalid header info... waiting.\n');
  end;
  pause(1);
end;

% set the real-time-clock to use
initgetwTime;
initsleepSec;

trlen_ms=600;
% ----------------------------------------------------------------------------
%    FILL IN YOUR CODE BELOW HERE
% ----------------------------------------------------------------------------
hdls = initGrid({'A' 'B'; 'C' 'D'})
for i = 1:4
  set(hdls(i), 'color', [1 1 1])
end

sendEvent('experiment.start', 1)
for sequence = 1:6
  target = randi([1 4])
  sendEvent('target', target)
  set(hdls(target), 'color', [0 1 0])
  sleep(2)
  set(hdls(target), 'color', [1 1 1])
  sleep(1)

  for trial = 1:5
    for letter = 1:4
      set(hdls(letter), 'color', [1 0 0])
      sendEvent('stimulus', letter==target)
      sleep(0.1)
      set(hdls(letter), 'color', [1 1 1])
      sleep(0.1)
    end
  end
end
sendEvent('experiment.end', 1)


% useful functions
% buffer_waitData(???)
