import React from 'react'

const Progress = ({ title, percentage, color }) => {

    const style = {
        'width': `${percentage}%`,
        backgroundColor: color
    }

    return (
        <div className='progress-wrap'>
            <div className='progress-holder progress'>
                <div className='progress' style={style} />
            </div>
            <div className='progress-text'
                style={{ color: color }}
            >
                {title}
            </div>
        </div>
    )
}

export default Progress