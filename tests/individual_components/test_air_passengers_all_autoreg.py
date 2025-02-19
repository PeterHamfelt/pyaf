import pyaf.ForecastEngine as autof
import pyaf.Bench.TS_datasets as tsds

b1 = tsds.load_airline_passengers()
df = b1.mPastData

def test_ar(iAR):
    lKnownTrends = ['LinearTrend']
    lKnownPeriodics = ['BestCycle']

    lEngine = autof.cForecastEngine()
    lEngine

    H = b1.mHorizon;
    lEngine.mOptions.set_active_transformations([ 'None' ]);
    lEngine.mOptions.set_active_trends(lKnownTrends);
    lEngine.mOptions.set_active_periodics(lKnownPeriodics);
    lEngine.mOptions.set_active_autoregressions([ iAR ]);
    lEngine.train(df , b1.mTimeVar , b1.mSignalVar, H);
    lEngine.getModelInfo();

    lEngine.standardPlots("outputs/my_airline_passengers_autoreg_" + iAR + "_")

    dfapp_in = df.copy();
    dfapp_in.tail()

    #H = 12
    dfapp_out = lEngine.forecast(dfapp_in, H);
    dfapp_out.tail(2 * H)
    print("Forecast Columns " , dfapp_out.columns);
    lForecastColumnName = b1.mSignalVar + '_Forecast'
    Forecast_DF = dfapp_out[[b1.mTimeVar , b1.mSignalVar, lForecastColumnName , lForecastColumnName + '_Lower_Bound',  lForecastColumnName + '_Upper_Bound' ]]
    print(Forecast_DF.info())
    print("Forecasts\n" , Forecast_DF.tail(2*H));

    print("\n\n<ModelInfo>")
    print(lEngine.to_json());
    print("</ModelInfo>\n\n")
    print("\n\n<Forecast>")
    print(Forecast_DF.tail(2*H).to_json(date_format='iso'))
    print("</Forecast>\n\n")



def test_all_ARs():
    import pyaf.TS.Options as tsopts
    lKnownARs = tsopts.cModelControl.gKnownAutoRegressions
    lKnownARs = [x for x in lKnownARs if not x.endswith('X')]
    for lAR in lKnownARs:
        test_ar(lAR)

test_all_ARs()
