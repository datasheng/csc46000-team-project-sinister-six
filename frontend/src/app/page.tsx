"use client";
import Visualization from "./Visualization";

const visPairs = [
  {
    vooTitle: "VOOTimeseries",
    rspTitle: "RSPTimeseries",
    conclusion: "put a conclusion here",
  },
  {
    vooTitle: "VOOLinearRegression",
    rspTitle: "RSPLinearRegression",
    conclusion: "put a conclusion here",
  },
  {
    vooTitle: "VOOVolumeByDate",
    rspTitle: "RSPVolumebyDate",
    conclusion: "put a conclusion here",
  },
  {
    vooTitle: "VOO7DayMovingAverage",
    rspTitle: "RSP7DayMovingAverage",
    conclusion: "put a conclusion here",
  },
  {
    vooTitle: "VOO30DayMovingAverage",
    rspTitle: "RSP30DayMovingAverage",
    conclusion: "put a conclusion here",
  },
];

const combinedVis = [
  {
    title: "VOOvsRSPTimeseries",
    conclusion: "put a conclusion here",
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
