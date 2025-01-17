import React from 'react'
import NavbarLink from './NavbarLink'

const NavigationBar = () => {
    return (
        <div id='navbar'>
            <div className='navtitle'>
                Forex Dash
            </div>
            <div id='navlinks'>
                <NavbarLink path="/" text="Home" />
                <NavbarLink path="/dashboard" text="Dashboard" />
            </div>
        </div>
    )
}

export default NavigationBar