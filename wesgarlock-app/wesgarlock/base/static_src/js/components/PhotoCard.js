import React from 'react'
import PropTypes from 'prop-types'
import { Card, withStyles } from '@material-ui/core'

const styles = (theme) => ({
  img: {
    width: '100%',
    height: 'auto',
    marginBottom: -5
  },
  card: {
    boxShadow: theme.shadows[2]
  },
  noDecoration: {
    textDecoration: 'none !important'
  },
  title: {
    transition: theme.transitions.create(['background-color'], {
      duration: theme.transitions.duration.complex,
      easing: theme.transitions.easing.easeInOut
    }),
    cursor: 'pointer',
    color: theme.palette.secondary.main,
    '&:hover': {
      color: theme.palette.secondary.dark
    },
    '&:active': {
      color: theme.palette.primary.dark
    }
  },
  link: {
    transition: theme.transitions.create(['background-color'], {
      duration: theme.transitions.duration.complex,
      easing: theme.transitions.easing.easeInOut
    }),
    cursor: 'pointer',
    color: theme.palette.primary.main,
    '&:hover': {
      color: theme.palette.primary.dark
    }
  },
  showFocus: {
    '&:focus span': {
      color: theme.palette.secondary.dark
    }
  }
})

function PhotoCard (props) {
  const { classes, src } = props
  return (
    <Card className={classes.card}>
      {src && (
          <img src={src} className={classes.img} alt=""/>
      )}
    </Card>
  )
}

PhotoCard.propTypes = {
  classes: PropTypes.object.isRequired,
  title: PropTypes.string.isRequired,
  src: PropTypes.string
}

export default withStyles(styles, { withTheme: true })(PhotoCard)
