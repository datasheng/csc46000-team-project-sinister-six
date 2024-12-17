"use client";
import Visualization from "./Visualization";

const visPairs = [
  {
    vooTitle: "VOOTimeseries",
    rspTitle: "RSPTimeseries",
    conclusion: "Over the 10-year period, VOO demonstrates a relatively stable upward trajectory compared to RSP, which exhibits more pronounced fluctuations. VOO is likely to maintain consistent growth due to its lower volatility, while RSP may continue its trend of higher risk and reward dynamics.",
  },
  {
    vooTitle: "VOOLinearRegression",
    rspTitle: "RSPLinearRegression",
    conclusion: "The linear regression for VOO indicates a steady growth trend with a higher slope than RSP, which shows slower, less consistent growth. VOO is expected to outperform RSP in long-term growth, assuming market conditions remain similar.",
  },
  {
    vooTitle: "VOOVolumeByDate",
    rspTitle: "RSPVolumebyDate",
    conclusion: "Trading volumes for both RSP and VOO show periodic spikes, with RSP experiencing higher volume variability compared to VOO's more stable volume trend. VOO's stable volume suggests continued investor confidence, while RSP's volume spikes could indicate speculative interest, leading to greater price swings.",
  },
  {
    vooTitle: "VOO7DayMovingAverage",
    rspTitle: "RSP7DayMovingAverage",
    conclusion: "The 7-day moving average for VOO shows smoother and more predictable trends, while RSP displays greater short-term volatility. VOO is likely to provide a steadier investment performance, whereas RSP might offer short-term opportunities for active traders due to its higher volatility.",
  },
  {
    vooTitle: "VOO30DayMovingAverage",
    rspTitle: "RSP30DayMovingAverage",
    conclusion: "The 30-day moving average reinforces the consistency of VOO's performance over time, highlighting a gradual growth pattern. RSP, while showing more pronounced fluctuations, indicates potential opportunities for investors seeking higher risks with possible rewards.",
  },
];

const combinedVis = [
  {
    title: "VOOvsRSPTimeseries",
    conclusion: "The dual-axis time series highlights VOO's steady and consistent upward trajectory, showcasing its resilience and reliability, whereas RSP demonstrates higher volatility with sharper peaks and troughs. This comparison suggests VOO is a safer long-term investment, while RSP offers opportunities for higher returns in shorter, more speculative windows.",
  },
];

export default function Home() {
  return (
    <div className="bg-primaryDark min-h-screen text-primaryLight flex flex-col text-center pt-10">
      <h1 className="text-6xl font-extrabold">Comparing Two ETFs</h1>
      <div className="flex-row flex justify-center text-4xl gap-8 pt-6 font-bold">
        <div className="border-2 border-primaryAccent rounded-3xl px-10 py-1">
          VOO
        </div>
        <div>vs</div>
        <div className="border-2 border-primaryAccent rounded-3xl px-10 py-1">
          RSP
        </div>
      </div>

      <div className="border-b border-primaryAccent w-3/5 mx-auto pt-10"></div>

      <div className="flex justify-center gap-8 p-8">
        <div className="flex flex-col gap-16">
          {visPairs.map((visPair) => (
            <div key={visPair.vooTitle} className="flex flex-col">
              <div className="flex">
                <div className="rounded-lg p-4 w-full">
                  <Visualization
                    src={`https://us-east-1.online.tableau.com/t/aandha000-f853a42765/views/VOOvsRSP/${visPair.vooTitle}`}
                  />
                </div>
                <div className="rounded-lg p-4 w-full">
                  <Visualization
                    src={`https://us-east-1.online.tableau.com/t/aandha000-f853a42765/views/VOOvsRSP/${visPair.rspTitle}`}
                  />
                </div>
              </div>
              <h2 className="text-4xl font-bold border-b border-gray-600 pb-4">
                {visPair.conclusion}
              </h2>
            </div>
          ))}

          {combinedVis.map((vis) => (
            <div key={vis.title} className="flex flex-col">
              <div className="rounded-lg p-4 w-full flex justify-center">
                <Visualization
                  src={`https://us-east-1.online.tableau.com/t/aandha000-f853a42765/views/VOOvsRSP/${vis.title}`}
                />
              </div>
              <h2 className="text-4xl font-bold border-b border-gray-600 pb-4">
                {vis.conclusion}
              </h2>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
