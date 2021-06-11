from config.config import SERVER_BACK

logoIMG = "https://www.dropbox.com/s/vonrx4kb0guddk1/logo-email.png?dl=1"


class UTemplates:
    def emailHtmlDefault(self):
        return (
            """<link rel="stylesheet" type="text/css" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css"><table style="width:645px;font-family:arial,sans-serif,tahoma;margin:0px;background:#474747"><tbody><tr><td colspan="4" style="border-bottom: 2px solid #474747;padding:10px;background:#fff"><a href="#" target="_blank" style="display: inline;text-decoration-line: none;"><img src="https://www.dropbox.com/s/du22pgt8wnw0yob/ProductLogo.png?dl=1" style="height: 93px;width: 100%;border: none;"></a></td></tr><tr><td colspan="4" style="background:#fff;padding:10px"><font size="2"><div>Estimado(a) <a style="color:#000022;">"""
            + self.info["name"]
            + """</a>,<br><p>Bienvenido a Calenbell</p><p>Nos alegra que seas parte de nosotros!, de ahoraen adelante tendrás disponible una agenda persolal que te seguirá todo el tiempo mientras estés en linea, si no hiciste este registro contáctanos, nosotros nos encargamos del resto :) , en Calenbell Estamos para lo que necesites</b></p></div>Atentamente<br><br>Equipo de Calenbell</font></td></tr></tbody></table>"""
        )

    def recoveryPwdHtml(self):
        return (
            """<link rel="stylesheet" type="text/css" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css"><table style="width:645px;font-family:arial,sans-serif,tahoma;margin:0px;background:#474747"><tbody><tr><td colspan="4" style="border-bottom: 2px solid #474747;padding:10px;background:#fff"><a href="#" target="_blank" style="display: inline;text-decoration-line: none;"><img src='"""
            + logoIMG
            + """' style="height: 93px;width: 100%;border: none;"></a></td></tr><tr><td colspan="4" style="background:#fff;padding:10px"><font size="2"><div>Estimado(a) <a style="color:#000022;">"""
            + self.info["name"]
            + """</a>,<br><p>Se ha solicitado recuperación de su contraseña</p><p>Nos alegra que seas parte de nosotros!, se acaba de solicitar reestablecimiento de tu contraseña, si no hiciste esta petición solo ignóralo, nosotros nos encargamos del resto :) , en Calenbell Estamos para lo que necesites, solo contáctanos!</b></p></div>Atentamente<br><br>Equipo de Calenbell</font></td></tr></tbody></table>"""
        )

    def recoveryPwdEmailHtml(self):
        return (
            """<link rel="stylesheet" type="text/css" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css"><table style="width:645px;font-family:arial,sans-serif,tahoma;margin:0px;background:#474747"><tbody><tr><td colspan="4" style="border-bottom: 2px solid #474747;padding:10px;background:#fff"><a href="#" target="_blank" style="display: inline;text-decoration-line: none;"><img src='"""
            + logoIMG
            + """' style="height: 93px;width: 100%;border: none;"></a></td></tr><tr><td colspan="4" style="background:#fff;padding:10px"><font size="2"><div>Estimado(a) <a style="color:#000022;">"""
            + self.info["name"]
            + """</a>,<br><p>Se ha solicitado recuperación de su contraseña</p><p>Código de recuperación: <b>"""
            + self.info["code"]
            + """</b></p><p>Nos alegra que seas parte de nosotros!, se acaba de solicitar reestablecimiento de tu contraseña, si no hiciste esta petición solo ignóralo, nosotros nos encargamos del resto :) , en Calenbell Estamos para lo que necesites, solo contáctanos!</b></p></div>Atentamente<br><br>Equipo de Calenbell</font></td></tr></tbody></table>"""
        )

    def sendQueryFriends(self):
        return (
            """<link rel="stylesheet" type="text/css" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css"><table style="width:645px;font-family:arial,sans-serif,tahoma;margin:0px;background:#474747"><tbody><tr><td colspan="4" style="border-bottom: 2px solid #474747;padding:10px;background:#fff"><a href="#" target="_blank" style="display: inline;text-decoration-line: none;"><img src='"""
            + logoIMG
            + """' style="height: 93px;width: 100%;border: none;"></a></td></tr><tr><td colspan="4" style="background:#fff;padding:10px; font-size: 15px;"><div>Estimado(a) <a style="color:#000022;">"""
            + self.info["name"]
            + """</a>,<br><p><img src='"""
            + self.info["photo_contact"]
            + """ ' style="height: 45px;width: 45px;border: none;"></p><p><b>"""
            + self.info["name_contact"]
            + """ </b>te ha enviado solicitud de amistad.</p><div><a href='"""
            + SERVER_BACK
            + """/user/manage/query/friends/"""
            + self.info["link_acepte"]
            + """'" style="text-decoration: none; color: #fff; background-color: #26a69a; text-align: center; letter-spacing: .5px;border: none; border-radius: 2px; height: 36px; line-height: 36px; padding: 0 16px; cursor: pointer;">Aceptar</a><a href='"""
            + SERVER_BACK
            + """/user/manage/query/friends/"""
            + self.info["link_decline"]
            + """'" style="text-decoration: none; color: #fff; background-color: #F44336; text-align: center; letter-spacing: .5px;border: none; border-radius: 2px; height: 36px; line-height: 36px; padding: 0 16px; cursor: pointer;">Rechazar</a><p>Nos alegra que seas parte de nosotros!, en Calenbell Estamos para lo que necesites, solo contáctanos!</b></p></div></div>Atentamente<br><br>Equipo de Calenbell</td></tr></tbody></table>"""
        )

    def sendQueryGroup(self):
        return (
            """<link rel="stylesheet" type="text/css" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css"><table style="width:645px;font-family:arial,sans-serif,tahoma;margin:0px;background:#474747"><tbody><tr><td colspan="4" style="border-bottom: 2px solid #474747;padding:10px;background:#fff"><a href="#" target="_blank" style="display: inline;text-decoration-line: none;"><img src='"""
            + logoIMG
            + """' style="height: 93px;width: 100%;border: none;"></a></td></tr><tr><td colspan="4" style="background:#fff;padding:10px; font-size: 15px;"><div>Estimado(a) <a style="color:#000022;">"""
            + self.info["name"]
            + """</a>,<br><p><img src='"""
            + self.info["photo_contact"]
            + """ ' style="height: 45px;width: 45px;border: none;"></p><p ><b>"""
            + self.info["name_contact"]
            + """ </b>te ha invitado al grupo <b>"""
            + self.info["group"]
            + """</b>.</p><div><a href='"""
            + SERVER_BACK
            + """/user/join/event/"""
            + self.info["link_acepte"]
            + """'" style='text-decoration: none; color: #fff; background-color: #26a69a; text-align: center; letter-spacing: .5px;border: none; border-radius: 2px; height: 36px; line-height: 36px; padding: 0 16px; cursor: pointer;'>Aceptar</a><a href='"""
            + SERVER_BACK
            + """/user/join/event/"""
            + self.info["link_decline"]
            + """'" style='text-decoration: none; color: #fff; background-color: #F44336; text-align: center; letter-spacing: .5px;border: none; border-radius: 2px; height: 36px; line-height: 36px; padding: 0 16px; cursor: pointer;'>Rechazar</a><p><i>La invitación expirará en 30 minutos.</i></p><p>Nos alegra que seas parte de nosotros!, en Calenbell Estamos para lo que necesites, solo contáctanos!</b></p></div></div>Atentamente<br><br>Equipo de Calenbell</td></tr></tbody></table>"""
        )

    def sendDeleteGroup(self):
        return (
            """<link rel="stylesheet" type="text/css" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css"><table style="width:645px;font-family:arial,sans-serif,tahoma;margin:0px;background:#474747"><tbody><tr><td colspan="4" style="border-bottom: 2px solid #474747;padding:10px;background:#fff"><a href="#" target="_blank" style='display: inline;text-decoration-line: none;'><img src='"""
            + logoIMG
            + """' style='height: 93px;width: 100%;border: none;'></a></td></tr><tr><td colspan='4' style='background:#fff;padding:10px; font-size: 15px;'><div>Estimado(a) <a style='color:#000022;'>"""
            + self.info["name"]
            + """</a>,<br><p><img src='"""
            + self.info["photo_contact"]
            + """ ' style='height: 45px;width: 45px;border: none;'></p><p><b>"""
            + self.info["name_contact"]
            + """ </b>te ha sacado del grupo <b>"""
            + self.info["group"]
            + """</b>.</p><div><p>Si crees que sea un error puedes contactarnos! y nos encargaremos del resto, en Calenbell estamos para lo que necesites</b></p></div></div>Atentamente<br><br>Equipo de Calenbell</td></tr></tbody></table>"""
        )
