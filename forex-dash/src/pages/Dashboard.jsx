import React, { useEffect, useState } from 'react'
import TitleHead from '../components/TitleHead'
import Select from '../components/Select'
import { COUNTS, GRANULARITIES, PAIRS } from '../app/data'
import Button from '../components/Button'
import endPoints from '../app/api'
import Technicals from '../components/Technicals'
import PriceChart from '../components/PriceChart'

const Dashboard = () => {

    const [selectedPair, setSelectedPair] = useState(null);
    const [selectedGran, setSelectedGran] = useState(null);
    const [technicalsData, setTechnicalsData] = useState(null);
    const [priceData, setPriceData] = useState(null);
    const [selectedCount, setSelectedCount] = useState(COUNTS[0].value);
    const [options, setOptions] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadOptions();
    }, [])

    const handleCountChange = (count) => {
        setSelectedCount(count);
        loadPrices(count);
    }

    const loadOptions = async () => {
        const data = await endPoints.options();
        setOptions(data);
        setSelectedGran(data.granularities[0].value);
        setSelectedPair(data.pairs[0].value);
        setLoading(false)
    }

    const loadPrices = async (count) => {
        const data = await endPoints.prices(selectedPair, selectedGran, count);
        setPriceData(data);
    }

    const loadTechnicals = async () => {
        const data = await endPoints.technicals(selectedPair, selectedGran);
        console.log({ ...data });
        setTechnicalsData(data);
        loadPrices(selectedCount);
    }

    if (loading == true) return <h1>Loading...</h1>

    return (
        <div>
            <TitleHead title='Options' />
            <div className='segment options'>
                <Select name="Currency" title="Select currency" options={options.pairs} defaultValue={selectedPair} onSelected={setSelectedPair} />
                <Select name="Granularity" title="Select granularity" options={options.granularities} defaultValue={selectedGran} onSelected={setSelectedGran} />
                <Button text="Load" handleClick={() => loadTechnicals()} />
            </div>
            <TitleHead title="Technicals" />
            {technicalsData && <Technicals data={technicalsData} />}
            <TitleHead title="Price Chart" />
            {priceData && <PriceChart
                selectedCount={selectedCount}
                selectedPair={selectedPair}
                selectedGranularity={selectedGran}
                handleCountChange={handleCountChange}
                priceData={priceData}
            />}
        </div>
    )
}

export default Dashboard