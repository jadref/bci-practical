clear configRun
configureSpeller;
startSigProcBuffer('epochEventType','stimulus.tgtFlash','freqband',freqband,...
                   'testepochEventType',{'stimulus.rowFlash' 'stimulus.colFlash' 'stimulus.flash'},...
                   'sendPredEventType','stimulus.sequence',...
                   'clsfr_type','erp','trlen_ms',trlen_ms,...
                   'calibrateOpts',calibrateOpts,'trainOpts',trainOpts,...
                   'contFeedbackOpts',contFeedbackOpts,...
                   'epochFeedbackOpts',epochFeedbackOpts,...
                   'useGUI',0);
