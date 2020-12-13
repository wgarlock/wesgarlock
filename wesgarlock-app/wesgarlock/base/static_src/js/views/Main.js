import React, { memo, useState, useCallback } from 'react'
import PropTypes from 'prop-types'
import AOS from 'aos/dist/aos'
import { withStyles } from '@material-ui/core'
import NavBar from './navigation/NavBar'
import Footer from './footer/Footer'
import 'aos/dist/aos.css'
import CookieRulesDialog from './cookies/CookieRulesDialog'
import CookieConsent from './cookies/CookieConsent'
import DialogSelector from './register_login/DialogSelector'

AOS.init({ once: true })

const styles = (theme) => ({
  wrapper: {
    backgroundColor: theme.palette.common.white,
    overflowX: 'hidden'
  }
})

function Main (props) {
  const { classes } = props
  const [selectedTab, setSelectedTab] = useState(null)
  const [isMobileDrawerOpen, setIsMobileDrawerOpen] = useState(false)
  const [dialogOpen, setDialogOpen] = useState(null)
  const [isCookieRulesDialogOpen, setIsCookieRulesDialogOpen] = useState(false)

  const openLoginDialog = useCallback(() => {
    setDialogOpen('login')
    setIsMobileDrawerOpen(false)
  }, [setDialogOpen, setIsMobileDrawerOpen])

  const closeDialog = useCallback(() => {
    setDialogOpen(null)
  }, [setDialogOpen])

  const openRegisterDialog = useCallback(() => {
    setDialogOpen('register')
    setIsMobileDrawerOpen(false)
  }, [setDialogOpen, setIsMobileDrawerOpen])

  const openTermsDialog = useCallback(() => {
    setDialogOpen('termsOfService')
  }, [setDialogOpen])

  const handleMobileDrawerOpen = useCallback(() => {
    setIsMobileDrawerOpen(true)
  }, [setIsMobileDrawerOpen])

  const handleMobileDrawerClose = useCallback(() => {
    setIsMobileDrawerOpen(false)
  }, [setIsMobileDrawerOpen])

  const openChangePasswordDialog = useCallback(() => {
    setDialogOpen('changePassword')
  }, [setDialogOpen])

  const handleCookieRulesDialogOpen = useCallback(() => {
    setIsCookieRulesDialogOpen(true)
  }, [setIsCookieRulesDialogOpen])

  const handleCookieRulesDialogClose = useCallback(() => {
    setIsCookieRulesDialogOpen(false)
  }, [setIsCookieRulesDialogOpen])

  return (
    <div className={classes.wrapper}>
      {!isCookieRulesDialogOpen && (
        <CookieConsent
          handleCookieRulesDialogOpen={handleCookieRulesDialogOpen}
        />
      )}
      <DialogSelector
        openLoginDialog={openLoginDialog}
        dialogOpen={dialogOpen}
        onClose={closeDialog}
        openTermsDialog={openTermsDialog}
        openRegisterDialog={openRegisterDialog}
        openChangePasswordDialog={openChangePasswordDialog}
      />
      <CookieRulesDialog
        open={isCookieRulesDialogOpen}
        onClose={handleCookieRulesDialogClose}
      />
      <NavBar
        selectedTab={selectedTab}
        selectTab={setSelectedTab}
        openLoginDialog={openLoginDialog}
        openRegisterDialog={openRegisterDialog}
        mobileDrawerOpen={isMobileDrawerOpen}
        handleMobileDrawerOpen={handleMobileDrawerOpen}
        handleMobileDrawerClose={handleMobileDrawerClose}
      />
      {props.children}
      <Footer />
    </div>
  )
}

Main.propTypes = {
  classes: PropTypes.object.isRequired,
  children: PropTypes.array
}

export default withStyles(styles, { withTheme: true })(memo(Main))
