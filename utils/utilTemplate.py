class UTemplates:

    def emailHtmlDefault(self):
        return """<link rel="stylesheet" type="text/css" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css">
        <tbody>
            <tr>
                <td height="50"></td>
            </tr>
            <tr>
                <td style="align-content: center;">
                    <table width="80%" cellpadding="0" cellspacing="0" style="border:1px solid #f1f2f5;background-color: #ffffff";margin-left:320px>
                        <tbody>
                            <tr>
                                <td colspan="3" height="60" 
                                    style="border-bottom:1px solid #eeeeee;padding-left:16px;align-content: left;background-color: bgcolor=#ffffff";";>
                                    <img src="https://i.postimg.cc/vTf4vZBF/logoimgd.png"
                                        width="100" height="41" style="display:block;width:100px;height:41px"
                                        class="CToWUd">
                                    <h2 style="color:#000">Racing-http</h2>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="3" height="20"></td>
                            </tr>
                            <tr>
                                <td width="20"></td>
                                <td style="align-content: left;">
                                    <table cellpadding="0" cellspacing="0" width="100%">
                                        <tbody>
                                            <tr>
                                                <td colspan="3" style="text-align:center">
                                                    <span
                                                        style="font-family:Helvetica,Arial,sans-serif;font-weight:bold;font-size:28px;line-height:28px;color:#333333">Welcome
                                                        Racing-http</span>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td colspan="3" height="20"></td>
                                            </tr>
                                            <tr>
                                                <td colspan="3" height="1" 
                                                    style="font-size:1px;line-height:1px;background-color: #eeeeee;">&nbsp;</td>
                                            </tr>
                                            <tr>
                                                <td colspan="3" height="20"></td>
                                            </tr>
                                            <tr>
                                                <td colspan="3">
                                                    <p
                                                        style="font-family:Helvetica,Arial,sans-serif;color:#494747;line-height:140%;text-align:center">
                                                        Bienvenido alegre  <a
                                                            href="#"
                                                            style="color:#093ada;text-decoration:none" target="_blank">"""+self.info['userRec']+""" </a>
                                                            nos alegra que te nos hayas unido a nuestro entorno de Racing-http
                                                            podras disfrutar de las mejores nuestras funcionalidad y nuestro entorno <a
                                                            href="#"
                                                            style="color:#093ada;text-decoration:none" target="_blank">Racing-http.</a>Estamos ansiosos de que puedas empezar</p>
                                                    <table width="100%" style="width:100%;">
                                                        <tbody style="align-content:center>"
                                                            <tr>
                                                                <td>
                                                                    <a href="#" style="font-family:Helvetica,Arial,sans-serif;width:50%;text-align:center;padding:12px 0;background-color:#093ada;border:1px solid #093ada;border-radius:8px;display:block;color:#ffffff;font-size:14px;font-weight:normal;text-decoration:none;margin-left:25%">Sign In</a>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td colspan="3" height="20"></td>
                                            </tr>
                                            <tr>
                                                <td colspan="3" style="text-align:center">
                                                    <span
                                                        style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#cccccc">El
                                                        Entorno y grupo Racing-http,</span>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                                <td width="20"></td>
                            </tr>
                            <tr>
                                <td colspan="3" height="20"></td>
                            </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            <tr>
                <td height="50">
    
                </td>
            </tr>
        </tbody>"""

    def recoveryPwdHtml(self):
        return """<link rel="stylesheet" type="text/css" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css"><table style="width:645px;font-family:arial,sans-serif,tahoma;margin:0px;background:#474747"><tbody><tr><td colspan="4" style="border-bottom: 2px solid #474747;padding:10px;background:#fff"><a href="#" target="_blank" style="display: inline;text-decoration-line: none;"><img src="https://LOGO.png" style="height: 93px;width: 90px;border: none;"><img src="https://NOMBRE_APP.png" style="margin-bottom: 25px;"></a></td></tr><tr><td colspan="4" style="background:#fff;padding:10px"><font size="2"><div>Estimado(a) <a style="color:#000022;">"""+self.info['name']+"""</a>,<br><p>Se ha solicitado recuperación de su contraseña</p><p>Nos alegra que seas parte de nosotros!, se acaba de solicitar reestablecimiento de tu contraseña, si no hiciste esta petición solo ignóralo, nosotros nos encargamos del resto :) , en Calenbell Estamos para lo que necesites, solo contáctanos!</b></p></div>Atentamente<br><br>Equipo de Calenbell</font></td></tr></tbody></table><table style="width:645px;border-left:2px solid #474747;border-right:2px solid #474747;border-bottom:2px solid #474747;font-family:arial,sans-serif,tahoma;margin:0px;background:#fff"><tbody><tr style="background:#fff"><td style="width:40px;padding:10px"><img src="https://LOGO.png" style="height: 43px;width: 51px;border: none;"></td><td style="font-size:12px;text-align:left"> Calenbell </td><td style="font-weight:bold;text-align:right"><a style="text-decoration:none;color:transparent;font-size:12px" href="#" target="_blank"><font size="3">-----</font></a></td><td style="width:40px;padding:10px"><a href="#" target="_blank"><i class="fas fa-envelope icon" style="float:right;border:none; font-size: 30px;color: #000022;"></i></a></td></tr></tbody></table>"""

    def recoveryPwdEmailHtml(self):
        return """<link rel="stylesheet" type="text/css" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css"><table style="width:645px;font-family:arial,sans-serif,tahoma;margin:0px;background:#474747"><tbody><tr><td colspan="4" style="border-bottom: 2px solid #474747;padding:10px;background:#fff"><a href="#" target="_blank" style="display: inline;text-decoration-line: none;"><img src="https://LOGO.png" style="height: 93px;width: 90px;border: none;"><img src="https://NOMBRE_APP.png" style="margin-bottom: 25px;"></a></td></tr><tr><td colspan="4" style="background:#fff;padding:10px"><font size="2"><div>Estimado(a) <a style="color:#000022;">"""+self.info['name']+"""</a>,<br><p>Se ha solicitado recuperación de su contraseña</p><p>Código de recuperación: <b>"""+self.info['code']+"""</b></p><p>Nos alegra que seas parte de nosotros!, se acaba de solicitar reestablecimiento de tu contraseña, si no hiciste esta petición solo ignóralo, nosotros nos encargamos del resto :) , en Calenbell Estamos para lo que necesites, solo contáctanos!</b></p></div>Atentamente<br><br>Equipo de Calenbell</font></td></tr></tbody></table><table style="width:645px;border-left:2px solid #474747;border-right:2px solid #474747;border-bottom:2px solid #474747;font-family:arial,sans-serif,tahoma;margin:0px;background:#fff"><tbody><tr style="background:#fff"><td style="width:40px;padding:10px"><img src="https://LOGO.png" style="height: 43px;width: 51px;border: none;"></td><td style="font-size:12px;text-align:left"> Calenbell </td><td style="font-weight:bold;text-align:right"><a style="text-decoration:none;color:transparent;font-size:12px" href="#" target="_blank"><font size="3">-----</font></a></td><td style="width:40px;padding:10px"><a href="#" target="_blank"><i class="fas fa-envelope icon" style="float:right;border:none; font-size: 30px;color: #000022;"></i></a></td></tr></tbody></table>"""


