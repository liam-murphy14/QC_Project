from AlgorithmImports import *

class GapDownHighVolume(QCAlgorithm):

    def Initialize(self):
        # initialization 
        # START MY SNIPPIT
        start_year, start_month, start_day = tuple([int(date_item) for date_item in self.GetParameter("start_date").split('-')])
        end_year, end_month, end_day = tuple([int(date_item) for date_item in self.GetParameter("end_date").split('-')])
        self.SetStartDate(start_year, start_month, start_day)
        self.SetEndDate(end_year, end_month, end_day)
        self.SetCash(int(self.GetParameter("start_cash")))
        # END MY SNIPPIT

        # universe
        self.UniverseSettings.Resolution = Resolution.Minute
        self.AddUniverse(self.high_volume_course_filter)
        self.last_closes = dict()

        # flags
        self.record_data = False
        self.check_prices = False

        # scheduling
        self.AddEquity('SPY', Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay('SPY'), self.TimeRules.AfterMarketOpen('SPY', 0), self.set_check_flag)
        self.Schedule.On(self.DateRules.EveryDay('SPY'), self.TimeRules.BeforeMarketClose('SPY', 10), self.Liquidate) # day trades only
        self.Schedule.On(self.DateRules.EveryDay('SPY'), self.TimeRules.BeforeMarketClose('SPY', 1), self.set_record_flag)

        # parameters
        self.min_dol_vol = 10_000_000
        self.max_price = 1_000
        self.gap_perc = float(self.GetParameter("gap_down_percent")) # possibly change to some percent of stddev
        

    def high_volume_course_filter(self, course):
        return [x.Symbol for x in course if x.DollarVolume > self.min_dol_vol and x.Price < self.max_price]

    def OnSecuritiesChanged(self, changes) -> None:
        for sec in changes.RemovedSecurities:
            if sec.Invested:
                self.Liquidate(sec.Symbol)
            if sec.Symbol in self.last_closes.keys():
                self.last_closes.pop(sec.Symbol)

    def OnData(self, data: Slice):
        # only record data at end of day
        if self.record_data:
            for symb_bar_pair in data.Bars:
                symb = symb_bar_pair.Key
                bar = symb_bar_pair.Value
                # save last close
                self.last_closes[symb] = bar.Close
            self.record_data = False
        # only buy at beginning of day
        if self.check_prices:
            to_buy_today = list()
            for symb_bar_pair in data.Bars:
                symb = symb_bar_pair.Key
                bar = symb_bar_pair.Value
                if symb in self.last_closes.keys():
                    gap_down_percent = (self.last_closes[symb] - bar.Open) / self.last_closes[symb]
                else:
                    gap_down_percent = -100
                    self.Log(f'bad key: {symb}')
                if gap_down_percent >= self.gap_perc:
                    # add to trades for day
                    to_buy_today.append((symb, self.last_closes[symb] * 0.9))
            # make portfolio targets and execute
            # uniform distribution
            if len(to_buy_today) > 0:
                port_targ = 0.95 / len(to_buy_today) # keep a tiny bit of cash
                pt_in_cash = port_targ * self.Portfolio.Cash
                for symb, lim_price in to_buy_today:
                    num_shares = pt_in_cash // lim_price
                    self.LimitOrder(symb, num_shares, lim_price)
                self.check_prices = False
            else:
                self.Log(f'no buy today: {self.Time}')

    def set_check_flag(self):
        self.check_prices = True

    def set_record_flag(self):
        self.record_data = True

