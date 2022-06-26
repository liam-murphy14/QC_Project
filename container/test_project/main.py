from AlgorithmImports import *
from Selection.FutureUniverseSelectionModel import FutureUniverseSelectionModel
import QuantConnect

class TestFutures(QCAlgorithm):

    def Initialize(self):

        self.SetStartDate(2010, 12, 20) 
        self.SetEndDate(2022, 1, 14)
        self.SetCash(100_000)

        self.SetUniverseSelection(FrontMonthFutureUniverseSelectionModel(self.SelectFutureChainSymbols))
        self.AddAlpha(SMATrendFollowingAlphaModel())
        self.SetPortfolioConstruction(SingleSharePortfolioConstructionModel())
        
    def SelectFutureChainSymbols(self, utcTime):
        return [ Symbol.Create(Futures.Metals.Gold, SecurityType.Future, Market.COMEX) ] # Symbol.Create(Futures.Grains.Corn, SecurityType.Future, Market.Globex), Symbol.Create(Futures.Energies.CrudeOilWTI, SecurityType.Future, Market.NYMEX), Symbol.Create(Futures.Financials.EuroDollar, SecurityType.Future, Market.Globex), Symbol.Create(Futures.Currencies.EUR, SecurityType.Future, Market.Globex) ]
        
class FrontMonthFutureUniverseSelectionModel(FutureUniverseSelectionModel):
    '''Creates futures chain universes that select the front month contract and runs a user
    defined futureChainSymbolSelector every day to enable choosing different futures chains'''
    def __init__(self, select_future_chain_symbols):
        super().__init__(timedelta(1), select_future_chain_symbols)

    def Filter(self, filter):
        '''Defines the futures chain universe filter'''
        return (filter.FrontMonth()
                      .OnlyApplyFilterAtMarketOpen())
                      
class SMATrendFollowingAlphaModel(AlphaModel):

    def __init__(self, period=50, resolution=Resolution.Daily):
        self.period = period 
        self.resolution = resolution
        self.pred_int = Time.Multiply(Extensions.ToTimeSpan(resolution), period)
        self.symbol_data_by_symbol = dict()
        resolutionString = Extensions.GetEnumString(resolution, Resolution)
        self.Name = f"{self.__class__.__name__} ({period}, {resolutionString})"
        
    def Update(self, algorithm, data):       
        insights = []
        
        for symbol_data in self.symbol_data_by_symbol.values():
            if symbol_data.sma.IsReady:

                if symbol_data.in_uptrend:
                    if symbol_data.sma < symbol_data.sma[1]:
                        insights.append(Insight.Price(symbolData.symbol, self.pred_int, InsightDirection.Down))
                        symbol_data.in_downtrend = True
                        symbol_data.in_uptrend = False
                elif symbol_data.in_downtrend:
                    if symbol_data.sma > symbol_data.sma[1]:
                        insights.append(Insight.Price(symbolData.symbol, self.pred_int, InsightDirection.Up))
                        symbol_data.in_downtrend = False
                        symbol_data.in_uptrend = True
                else:
                    if symbol_data.sma < symbol_data.sma[1]:
                        insights.append(Insight.Price(symbolData.symbol, self.pred_int, InsightDirection.Down))
                        symbol_data.in_downtrend = True
                        symbol_data.in_uptrend = False
                    elif symbol_data.sma > symbol_data.sma[1]:
                        insights.append(Insight.Price(symbolData.symbol, self.pred_int, InsightDirection.Up))
                        symbol_data.in_downtrend = False
                        symbol_data.in_uptrend = True
        return insights
        
    def OnSecuritiesChanged(self, algorithm, changes):
        for security in changes.AddedSecurities:
            symbol_data = self.symbol_data_by_symbol.get(security.Symbol)

            if symbol_data is None:
                symbol_data = SymbolData(security)
                symbol_data.sma = algorithm.SMA(security.Symbol, self.period, self.resolution)
                self.symbol_data_by_symbol[security.Symbol] = symbol_data
            else:
                symbol_data.sma.Reset()

class SymbolData:
    def __init__(self, security):
        self.security = security
        self.symbol = security.Symbol
        self.sma = None
        self.in_uptrend = False
        self.in_downtrend = False
        self.atr = None

class FuturesVolatilityParityContructionModel(PortfolioConstructionModel):

    def __init__(self):
        self.symbol_data_by_symbol = dict()

    def OnSecuritiesChanged(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:

        for added in changes.Added F CU CKJDFLKJSLD:KFKDJS:
        return super().OnSecuritiesChanged(algorithm, changes)
    def CreateTargets(self, algorithm, insights):
        targets = []
        for insight in insights:
            if algorithm.Securities[insight.Symbol].IsTradable:
                targets.append(PortfolioTarget(insight.Symbol, insight.Direction * ))
        return targets
