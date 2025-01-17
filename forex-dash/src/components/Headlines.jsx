import React, { useEffect, useState } from 'react'
import TitleHead from './TitleHead'
import endPoints from '../app/api';
import Headline from './Headline';

const Headlines = () => {

    const [headlines, setHeadlines] = useState(null);

    useEffect(() => {
        loadHeadlines();
    }, [])

    const loadHeadlines = async () => {
        const data = await endPoints.headlines();
        setHeadlines(data);
    }

    return (
        <div>
            <TitleHead title="Headlines" />
            <div className='segment'>
                {
                    headlines && headlines.map((item, index) => {
                        return (
                            <Headline data={item} />

                        )
                    })
                }

            </div>
        </div>
    )
}

export default Headlines