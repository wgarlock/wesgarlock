/* global context */

import React, { memo } from 'react'
import PropTypes from 'prop-types'
import {
  AppBar,
  Toolbar,
  Button,
  Hidden,
  IconButton,
  withStyles,
  Link
} from '@material-ui/core'
import MenuIcon from '@material-ui/icons/Menu'
import HomeIcon from '@material-ui/icons/Home'
import HowToRegIcon from '@material-ui/icons/HowToReg'
import LockOpenIcon from '@material-ui/icons/LockOpen'
import NavigationDrawer from '../../components/NavigationDrawer'

const styles = theme => ({
  appBar: {
    boxShadow: theme.shadows[6],
    backgroundColor: theme.palette.common.white
  },
  toolbar: {
    display: 'flex',
    justifyContent: 'space-between'
  },
  logo: {
    height: '50px',
    width: 'auto'
  },
  menuButtonText: {
    fontSize: theme.typography.body1.fontSize,
    fontWeight: theme.typography.h6.fontWeight
  },
  brandText: {
    fontFamily: "'Baloo Bhaijaan', cursive",
    fontWeight: 400
  },
  noDecoration: {
    textDecoration: 'none !important'
  }
})

function NavBar (props) {
  const {
    classes,
    openRegisterDialog,
    openLoginDialog,
    handleMobileDrawerOpen,
    handleMobileDrawerClose,
    mobileDrawerOpen,
    selectedTab
  } = props

  let menuItems = []

  context.site.navigation.forEach(item => {
    menuItems.push({
      link: item.url,
      name: item.title,
      icon: <HomeIcon className="text-white" />
    })
  })

  if (!context.is_authenticated) {
    menuItems = [
      ...menuItems,
      {
        name: 'Register',
        onClick: openRegisterDialog,
        icon: <HowToRegIcon className="text-white" />
      },
      {
        name: 'Login',
        onClick: openLoginDialog,
        icon: <LockOpenIcon className="text-white" />
      }
    ]
  } else {
    menuItems = [
      ...menuItems,
      {
        name: 'Logout',
        link: context.front_urls.front_logout,
        icon: <HowToRegIcon className="text-white" />
      }
    ]
  }

  return (
    <div className={classes.root}>
      <AppBar position="fixed" className={classes.appBar}>
        <Toolbar className={classes.toolbar}>
          <div>
            <img className={classes.logo} src={context.site.logo.jpeg_400}/>
          </div>
          <div>
            <Hidden mdUp>
              <IconButton
                className={classes.menuButton}
                onClick={handleMobileDrawerOpen}
                aria-label="Open Navigation"
              >
                <MenuIcon color="primary" />
              </IconButton>
            </Hidden>
            <Hidden smDown>
              {menuItems.map(element => {
                if (element.link) {
                  return (
                    <Link href={element.link} key={element.name}>
                      <Button
                        color="secondary"
                        size="large"
                        classes={{ text: classes.menuButtonText }}
                      >
                        {element.name}
                      </Button>
                      </Link>

                  )
                }
                return (
                  <Link key={element.name}>
                    <Button
                      color="secondary"
                      size="large"
                      onClick={element.onClick}
                      classes={{ text: classes.menuButtonText }}
                      key={element.name}
                    >
                      {element.name}
                    </Button>
                  </Link>
                )
              })}
            </Hidden>
          </div>
        </Toolbar>
      </AppBar>
      <NavigationDrawer
        menuItems={menuItems}
        anchor="right"
        open={mobileDrawerOpen}
        selectedItem={selectedTab}
        onClose={handleMobileDrawerClose}
      />
    </div>
  )
}

NavBar.propTypes = {
  classes: PropTypes.object.isRequired,
  handleMobileDrawerOpen: PropTypes.func,
  handleMobileDrawerClose: PropTypes.func,
  mobileDrawerOpen: PropTypes.bool,
  selectedTab: PropTypes.string,
  openRegisterDialog: PropTypes.func.isRequired,
  openLoginDialog: PropTypes.func.isRequired
}

export default withStyles(styles, { withTheme: true })(memo(NavBar))
