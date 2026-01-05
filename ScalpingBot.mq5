//+------------------------------------------------------------------+
//|                                                  ScalpingBot.mq5 |
//|                                  Copyright 2023, Jules Assistant |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2023, Jules Assistant"
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict

//--- Input parameters
input double   InpLotSize     = 0.01;        // Lot size
input int      InpStopLoss    = 50;          // Stop Loss (in points)
input int      InpTakeProfit  = 50;          // Take Profit (in points)
input int      InpMaxSpread   = 10;          // Max Spread (in points)
input int      InpStartHour   = 8;           // Start Trading Hour (server time)
input int      InpEndHour     = 20;          // End Trading Hour (server time)
input int      InpMagicNum    = 123456;      // Magic Number
input int      InpRSIPeriod   = 14;          // RSI Period
input int      InpRSILower    = 30;          // RSI Oversold Level
input int      InpRSIUpper    = 70;          // RSI Overbought Level

//--- Global variables
int            handle_rsi;                   // Handle for RSI indicator
double         rsi_buffer[];                 // Buffer for RSI values

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   //--- Initialize RSI handle
   handle_rsi = iRSI(_Symbol, _Period, InpRSIPeriod, PRICE_CLOSE);
   if(handle_rsi == INVALID_HANDLE)
     {
      Print("Failed to create RSI handle");
      return(INIT_FAILED);
     }

   //--- Array indexing as time series
   ArraySetAsSeries(rsi_buffer, true);

   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   //--- Release indicator handle
   IndicatorRelease(handle_rsi);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   //--- Check Trading Hours (Server Time)
   datetime time = TimeCurrent();
   MqlDateTime dt;
   TimeToStruct(time, dt);

   bool isTradingHours = (dt.hour >= InpStartHour && dt.hour < InpEndHour);

   //--- Close all positions if outside trading hours (No overnight)
   if(!isTradingHours)
     {
      CloseAllPositions();
      return;
     }

   //--- Check for open positions
   if(PositionsTotal() > 0)
      return; // Simple logic: one trade at a time

   //--- Check Spread
   double spread = SymbolInfoInteger(_Symbol, SYMBOL_SPREAD);
   if(spread > InpMaxSpread)
      return; // Spread too high

   //--- Get RSI Data
   if(CopyBuffer(handle_rsi, 0, 0, 2, rsi_buffer) < 2)
      return;

   double rsi_curr = rsi_buffer[0];
   double rsi_prev = rsi_buffer[1];

   //--- Trading Logic (Scalping Reversal)
   // Buy Signal: RSI crosses above lower level (30)
   if(rsi_prev < InpRSILower && rsi_curr >= InpRSILower)
     {
      OpenBuy();
     }
   // Sell Signal: RSI crosses below upper level (70)
   else if(rsi_prev > InpRSIUpper && rsi_curr <= InpRSIUpper)
     {
      OpenSell();
     }
  }

//+------------------------------------------------------------------+
//| Open Buy Position                                                |
//+------------------------------------------------------------------+
void OpenBuy()
  {
   MqlTradeRequest request={0};
   MqlTradeResult  result={0};

   request.action       = TRADE_ACTION_DEAL;
   request.symbol       = _Symbol;
   request.volume       = InpLotSize;
   request.type         = ORDER_TYPE_BUY;
   request.price        = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   request.deviation    = 10;
   request.magic        = InpMagicNum;

   // Calculate SL/TP
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   if(InpStopLoss > 0)
      request.sl = request.price - InpStopLoss * point;
   if(InpTakeProfit > 0)
      request.tp = request.price + InpTakeProfit * point;

   if(!OrderSend(request, result))
      Print("OrderSend error: ", result.retcode);
  }

//+------------------------------------------------------------------+
//| Open Sell Position                                               |
//+------------------------------------------------------------------+
void OpenSell()
  {
   MqlTradeRequest request={0};
   MqlTradeResult  result={0};

   request.action       = TRADE_ACTION_DEAL;
   request.symbol       = _Symbol;
   request.volume       = InpLotSize;
   request.type         = ORDER_TYPE_SELL;
   request.price        = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   request.deviation    = 10;
   request.magic        = InpMagicNum;

   // Calculate SL/TP
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   if(InpStopLoss > 0)
      request.sl = request.price + InpStopLoss * point;
   if(InpTakeProfit > 0)
      request.tp = request.price - InpTakeProfit * point;

   if(!OrderSend(request, result))
      Print("OrderSend error: ", result.retcode);
  }

//+------------------------------------------------------------------+
//| Close All Positions                                              |
//+------------------------------------------------------------------+
void CloseAllPositions()
  {
   for(int i=PositionsTotal()-1; i>=0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(PositionSelectByTicket(ticket))
        {
         if(PositionGetInteger(POSITION_MAGIC) == InpMagicNum)
           {
            MqlTradeRequest request={0};
            MqlTradeResult  result={0};

            request.action = TRADE_ACTION_DEAL;
            request.position = ticket;
            request.symbol = PositionGetString(POSITION_SYMBOL);
            request.volume = PositionGetDouble(POSITION_VOLUME);
            request.deviation = 10;
            request.magic = InpMagicNum;

            if(PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
              {
               request.type = ORDER_TYPE_SELL;
               request.price = SymbolInfoDouble(request.symbol, SYMBOL_BID);
              }
            else
              {
               request.type = ORDER_TYPE_BUY;
               request.price = SymbolInfoDouble(request.symbol, SYMBOL_ASK);
              }

            if(!OrderSend(request, result))
               Print("OrderClose error: ", result.retcode);
           }
        }
     }
  }
//+------------------------------------------------------------------+
