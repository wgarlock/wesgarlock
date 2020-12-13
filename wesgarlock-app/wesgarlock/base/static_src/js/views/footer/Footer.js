/* global context */

import React, { useState } from 'react'
import PropTypes from 'prop-types'
import {
  Grid,
  Typography,
  Box,
  IconButton,
  Hidden,
  withStyles,
  withWidth,
  isWidthUp,
  TextField
} from '@material-ui/core'
import PhoneIcon from '@material-ui/icons/Phone'
import MailIcon from '@material-ui/icons/Mail'
import WaveBorder from '../../components/WaveBorder'
import transitions from '@material-ui/core/styles/transitions'
import ColoredButton from '../../components/ColoredButton'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { request } from '../../api/request'
import Toast from '../../components/Toast'

const styles = theme => ({
  footerInner: {
    backgroundColor: theme.palette.common.darkBlack,
    paddingTop: theme.spacing(8),
    paddingLeft: theme.spacing(2),
    paddingRight: theme.spacing(2),
    paddingBottom: theme.spacing(6),
    [theme.breakpoints.up('sm')]: {
      paddingTop: theme.spacing(10),
      paddingLeft: theme.spacing(16),
      paddingRight: theme.spacing(16),
      paddingBottom: theme.spacing(10)
    },
    [theme.breakpoints.up('md')]: {
      paddingTop: theme.spacing(10),
      paddingLeft: theme.spacing(10),
      paddingRight: theme.spacing(10),
      paddingBottom: theme.spacing(10)
    }
  },
  brandText: {
    fontFamily: "'Baloo Bhaijaan', cursive",
    fontWeight: 400,
    color: theme.palette.common.white
  },
  footerLinks: {
    marginTop: theme.spacing(2.5),
    marginBot: theme.spacing(1.5),
    color: theme.palette.common.white
  },
  infoIcon: {
    color: `${theme.palette.common.white} !important`,
    backgroundColor: '#33383b !important'
  },
  socialIcon: {
    fill: theme.palette.common.white,
    backgroundColor: 'transparent',
    borderRadius: theme.shape.borderRadius,
    color: '#ffffff',
    '&:hover': {
      color: theme.palette.primary.light
    }
  },
  link: {
    cursor: 'Pointer',
    color: theme.palette.common.white,
    transition: transitions.create(['color'], {
      duration: theme.transitions.duration.shortest,
      easing: theme.transitions.easing.easeIn
    }),
    '&:hover': {
      color: theme.palette.primary.light
    }
  },
  whiteBg: {
    backgroundColor: theme.palette.common.white
  }
})

const infos = []

if (context.site.site_phone) {
  infos.push(
    {
      icon: <PhoneIcon />,
      description: context.site.site_phone || ''
    }
  )
}

if (context.site.site_email) {
  infos.push(
    {
      icon: <MailIcon />,
      description: context.site.site_email || ''
    }
  )
}

const socialIcons = []

if (Array.isArray(context.site.social_media)) {
  context.site.social_media.forEach(item => {
    socialIcons.push({
      icon: item.icon,
      label: item.label,
      href: item.url
    })
  })
}

function Footer (props) {
  const { classes, theme, width } = props
  const [message, setMessage] = useState('')
  const [severity, setSeverity] = useState('')
  const [openToast, setOpenToast] = useState(false)
  const duration = 3000

  function handleMessage (e) {
    const form = e.target
    const email = e.target.elements.email.value
    const body = e.target.elements.body.value
    const url = context.front_urls.front_message_post
    request({ url: url, method: 'POST', body: { email: email, body: body } }).then(data => {
      const response = JSON.parse(data)
      form.reset()
      setMessage(response)
      setSeverity('success')
      setOpenToast(true)
    }).catch(err => {
      const response = JSON.parse(err)
      setMessage(response)
      setSeverity('error')
      setOpenToast(true)
    })
  }

  return (
    <footer className="lg-p-top">
      <WaveBorder
        upperColor="#FFFFFF"
        lowerColor={theme.palette.common.darkBlack}
        animationNegativeDelay={4}
      />
      <div className={classes.footerInner}>
        <Grid container spacing={isWidthUp('md', width) ? 10 : 5}>
          <Grid item xs={12} md={6} lg={4}>
            <form onSubmit={(e) => { e.preventDefault(); handleMessage(e) }}>
              <Box display="flex" flexDirection="column">
                <Toast open={openToast} message={message} duration={duration} severity={severity} handleClose={() => { setOpenToast(false) }}/>
                <Box mb={1}>
                  <TextField
                    variant="outlined"
                    multiline
                    placeholder="Get in touch with us"
                    inputProps={{ 'aria-label': 'Get in Touch' }}
                    InputProps={{
                      className: classes.whiteBg
                    }}
                    rows={4}
                    fullWidth
                    required
                    name="body"
                  />
                </Box>
                <Box mb={1}>
                  <TextField
                    variant="outlined"
                    multiline
                    placeholder="Your Email"
                    inputProps={{ 'aria-label': 'Get in Touch' }}
                    InputProps={{
                      className: classes.whiteBg
                    }}
                    rows={1}
                    fullWidth
                    required
                    name="email"
                  />
                </Box>
                <ColoredButton
                  color={theme.palette.common.white}
                  variant="outlined"
                  type="submit"
                >
                  Send Message
                </ColoredButton>
              </Box>
            </form>
          </Grid>
          <Hidden mdDown>
            <Grid item xs={12} md={6} lg={4}>
              <Box display="flex" justifyContent="center">
                <div>
                  {infos.map((info, index) => (
                    <Box display="flex" mb={1} key={index}>
                      <Box mr={2}>
                        <IconButton
                          className={classes.infoIcon}
                          tabIndex={-1}
                          disabled
                        >
                          {info.icon}
                        </IconButton>
                      </Box>
                      <Box
                        display="flex"
                        flexDirection="column"
                        justifyContent="center"
                      >
                        <Typography variant="h6" className="text-white">

                        </Typography>
                      </Box>
                    </Box>
                  ))}
                </div>
              </Box>
            </Grid>
          </Hidden>
          <Grid item xs={12} md={6} lg={4}>
            <Typography style={{ color: '#8f9296' }} paragraph>
              {context.site.footer_content}
            </Typography>
            <Box display="flex">
              {socialIcons.map((socialIcon, index) => (
                <Box key={index} mr={index !== socialIcons.length - 1 ? 1 : 0}>
                  <IconButton
                    aria-label={socialIcon.label}
                    className={classes.socialIcon}
                    href={socialIcon.href}
                  >
                    <FontAwesomeIcon icon={['fab', socialIcon.icon]} />
                  </IconButton>
                </Box>
              ))}
            </Box>
          </Grid>
        </Grid>
      </div>
    </footer>
  )
}

Footer.propTypes = {
  theme: PropTypes.object.isRequired,
  classes: PropTypes.object.isRequired,
  width: PropTypes.string.isRequired,
  setDuration: PropTypes.func
}

export default withWidth()(withStyles(styles, { withTheme: true })(Footer))
