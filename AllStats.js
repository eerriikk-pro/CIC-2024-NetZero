

// props = {}
const allStatsComponent = (props) => {
   const inputArray = [
      ["1080-1800J", "Average query energy consumption", "Citing: Energy Consumption of ChatGPT Responses | Baeldung on Computer Science " ],
      ["72360J", "Initial for RAG Embedding", "Assuming 20 pages = 10,000 words ~= 67-100 paragraphs * 1080J"],
      ["64 queries = 69120J", "Developer cost", "Intense coding sessions developers make a query every 10-15 minutes, average of 4 team members"],
      ["3", "Average GenAi functions Per Use", "Taken from analyzing project Github"],
      ["93.9kg", "CO2 per KJ of electrical energy generation", "2022 U.S. Energy Information Administration"]
   ];
   return (
      <div className="allStats">
      {inputArray.map((prompt, index) => (
         <div className="dualBox">
         <h2 className="statNumber">prompt[0]</h2>
         <div>
            <h2 className="statLabel">prompt[1]</h2>
            <p>prompt[2]</p>
         </div>
         </div>
       ))} 
       
       <div className="TotalCost">
         <h2 className="statLabel">Static Cost</h2>
         <h3>141480 Joules</h3>
       </div>
       <div className="TotalCost">
         <h2 className="statLabel">Cost Per Use</h2>
         <h3>5400 Joules</h3>
       </div>

       <div className="ImagePlots">
         <div className="dualBox">
            <img alt="RunsOfProject_KJEmissions.png"></img>
            <p>93.9kg of CO2 produced per KJ of electricity generated. - 2022 U.S. Energy Information Administration </p>
         </div>
         <div>
            <img alt="ImpactDistributions.png"></img>
            <p>Berthelot et al. 2024</p>
         </div>
       </div>
      </div>
   )
}

export default allStatsComponent